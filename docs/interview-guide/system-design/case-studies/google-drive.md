---
sidebar_position: 9
title: "Design Google Drive — Cloud Storage"
description: >-
  Complete system design for Google Drive/Dropbox. File sync, versioning,
  sharing, and conflict resolution.
keywords:
  - design google drive
  - design dropbox
  - file sync
  - cloud storage
  - file sharing
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Building Blocks
  - Databases
companies: [Google, Dropbox, Microsoft, Box]
---

# Design Google Drive: Sync Everything

Cloud storage seems simple: upload files, download files. The complexity: sync across devices, handle conflicts, and scale to billions of files.

---

## Requirements

### Functional
- Upload/download files
- Sync across devices
- File/folder sharing
- Version history
- Offline access
- Real-time collaboration

### Non-Functional
- **Reliability:** No data loss (99.999999999% durability)
- **Availability:** 99.9%
- **Sync latency:** < 5 seconds for small files
- **Scale:** 1B users, 10PB new data daily

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Desktop/Mobile Clients                        │
│  (Watches file system, syncs changes, handles offline)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                               │
└─────────────────────────────────────────────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Upload    │        │    Sync     │        │   Sharing   │
│   Service   │        │   Service   │        │   Service   │
└──────┬──────┘        └──────┬──────┘        └─────────────┘
       │                      │
       ▼                      ▼
┌─────────────┐        ┌─────────────┐
│   Block     │        │  Metadata   │
│   Storage   │        │   Service   │
│   (S3)      │        │ (DB+Cache)  │
└─────────────┘        └─────────────┘
```

---

## Client Architecture

```
Desktop Client Components:
┌─────────────────────────────────────────────────────────────────┐
│                      Desktop Client                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ File Watcher │  │  Sync Engine │  │ Local DB     │          │
│  │ (inotify/    │  │ (Chunking,   │  │ (SQLite)     │          │
│  │  FSEvents)   │  │  Diff, Merge)│  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Upload Queue │  │ Download     │  │ Conflict     │          │
│  │              │  │ Manager      │  │ Resolver     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Chunking & Deduplication

```
Large File Upload:
┌─────────────────────────────────────────────────────────────────┐
│  Original File (100MB)                                          │
├─────────────────────────────────────────────────────────────────┤
│  [Chunk 1] [Chunk 2] [Chunk 3] ... [Chunk N]                   │
│   (4MB)     (4MB)     (4MB)         (4MB)                      │
└─────────────────────────────────────────────────────────────────┘

Each chunk:
1. Compute hash (SHA-256)
2. Check if hash exists in storage (dedup)
3. If new, upload and store
4. If exists, just reference existing chunk
```

### Benefits

```
Deduplication:
- Same file uploaded by different users → stored once
- File edited slightly → only changed chunks uploaded

Example:
- 100MB file, 1 line changed
- Only 1 chunk (4MB) uploaded instead of 100MB
```

---

## Sync Protocol

### Upload Flow

```
1. Client detects file change
   │
   ▼
2. Client computes file hash and chunk hashes
   │
   ▼
3. Client sends metadata to Sync Service
   {file_path, file_hash, chunk_hashes[], modified_time}
   │
   ▼
4. Sync Service responds with needed chunks
   (chunks that don't exist or differ)
   │
   ▼
5. Client uploads only needed chunks
   │
   ▼
6. Sync Service updates metadata DB
   │
   ▼
7. Sync Service notifies other clients via WebSocket
```

### Download Flow

```
1. Client receives notification of remote change
   │
   ▼
2. Client requests file metadata
   │
   ▼
3. Client compares chunk hashes
   │
   ▼
4. Client downloads only missing/changed chunks
   │
   ▼
5. Client assembles file from chunks
   │
   ▼
6. Client updates local DB
```

---

## Conflict Resolution

```
Scenario:
- Device A and B both modify same file offline
- Both come online and try to sync

Resolution:
1. Server accepts first sync
2. Second sync detects conflict (version mismatch)
3. Create conflict copy: "file.txt" and "file (conflict).txt"
4. Let user resolve manually

Alternative (for collaborative docs):
- Operational Transform (OT)
- Conflict-free Replicated Data Types (CRDTs)
```

---

## Metadata Schema

```sql
-- Files/Folders
CREATE TABLE files (
    file_id UUID PRIMARY KEY,
    user_id UUID,
    parent_id UUID,  -- Folder containing this file
    name VARCHAR(255),
    is_folder BOOLEAN,
    size BIGINT,
    file_hash VARCHAR(64),
    version INT,
    created_at TIMESTAMP,
    modified_at TIMESTAMP,
    deleted_at TIMESTAMP  -- Soft delete
);

-- Chunks
CREATE TABLE chunks (
    chunk_hash VARCHAR(64) PRIMARY KEY,
    size INT,
    storage_path VARCHAR(500),
    reference_count INT  -- For garbage collection
);

-- File-Chunk mapping
CREATE TABLE file_chunks (
    file_id UUID,
    chunk_index INT,
    chunk_hash VARCHAR(64),
    PRIMARY KEY (file_id, chunk_index)
);

-- Version history
CREATE TABLE file_versions (
    file_id UUID,
    version INT,
    chunk_hashes TEXT[],  -- Ordered list
    created_at TIMESTAMP,
    created_by UUID,
    PRIMARY KEY (file_id, version)
);
```

---

## Sharing

```
Share Types:
- View only
- Edit
- Comment only

Implementation:
┌─────────────────────────────────────────────────────────────────┐
│ Permissions Table                                                │
├─────────────────────────────────────────────────────────────────┤
│ file_id | user_id/email | permission | created_by | expires_at │
└─────────────────────────────────────────────────────────────────┘

Share link:
- Generate unique token
- Associate with file_id and permission
- Token can be revoked or time-limited
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Chunking | 4MB chunks | Balance upload size vs overhead |
| Dedup | Content-addressed | Save storage, fast sync |
| Sync notification | WebSocket | Real-time push |
| Conflict handling | Copy + manual | Simple, predictable |
| Storage | S3 | Durability, scale |

---

## Key Takeaways

1. **Chunking enables efficient sync**—only changed parts transfer.
2. **Content-addressed storage** provides automatic deduplication.
3. **WebSocket for real-time** sync notifications.
4. **Conflict copies** are simpler than automatic merging.
5. **Version history** by storing chunk lists per version.
