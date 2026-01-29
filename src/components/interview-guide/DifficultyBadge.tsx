import React from 'react';
import styles from './DifficultyBadge.module.css';

type DifficultyLevel = 'easy' | 'medium' | 'hard' | 'beginner' | 'intermediate' | 'advanced';

type DifficultyBadgeProps = {
  level: DifficultyLevel;
  showLabel?: boolean;
};

const DIFFICULTY_CONFIG: Record<DifficultyLevel, { emoji: string; label: string; className: string }> = {
  easy: { emoji: '🟢', label: 'Easy', className: 'easy' },
  beginner: { emoji: '🟢', label: 'Beginner', className: 'easy' },
  medium: { emoji: '🟡', label: 'Medium', className: 'medium' },
  intermediate: { emoji: '🟡', label: 'Intermediate', className: 'medium' },
  hard: { emoji: '🔴', label: 'Hard', className: 'hard' },
  advanced: { emoji: '🔴', label: 'Advanced', className: 'hard' },
};

/**
 * Visual difficulty indicator for problems and topics.
 * 
 * Usage:
 * <DifficultyBadge level="medium" />
 * <DifficultyBadge level="hard" showLabel={false} />
 */
export function DifficultyBadge({ level, showLabel = true }: DifficultyBadgeProps) {
  const config = DIFFICULTY_CONFIG[level];
  
  return (
    <span 
      className={`${styles.badge} ${styles[config.className]}`}
      title={config.label}
    >
      <span className={styles.emoji}>{config.emoji}</span>
      {showLabel && <span className={styles.label}>{config.label}</span>}
    </span>
  );
}

export type { DifficultyLevel };
