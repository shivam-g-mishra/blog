import React from 'react';
import styles from './ConfidenceBuilder.module.css';

type ConfidenceBuilderProps = {
  /** The type of confidence builder */
  type: 'youve-got-this' | 'dont-worry' | 'real-talk' | 'remember';
  /** The title (optional, has defaults based on type) */
  title?: string;
  /** The content to display */
  children: React.ReactNode;
};

const TYPE_CONFIG = {
  'youve-got-this': {
    icon: '💪',
    defaultTitle: "You've Got This",
    className: 'success',
  },
  'dont-worry': {
    icon: '🎯',
    defaultTitle: "Don't Worry If...",
    className: 'info',
  },
  'real-talk': {
    icon: '💬',
    defaultTitle: 'Real Talk',
    className: 'neutral',
  },
  'remember': {
    icon: '🧠',
    defaultTitle: 'Remember',
    className: 'primary',
  },
};

/**
 * Confidence-building callout boxes for reducing interview anxiety.
 * Use throughout the interview guide to encourage and reassure readers.
 * 
 * Usage:
 * <ConfidenceBuilder type="youve-got-this">
 *   Most candidates overthink this problem...
 * </ConfidenceBuilder>
 * 
 * <ConfidenceBuilder type="dont-worry">
 *   - You don't immediately see the optimal solution
 *   - You need to think out loud for 30 seconds
 * </ConfidenceBuilder>
 */
export function ConfidenceBuilder({ type, title, children }: ConfidenceBuilderProps) {
  const config = TYPE_CONFIG[type];
  const displayTitle = title || config.defaultTitle;
  
  return (
    <div className={`${styles.container} ${styles[config.className]}`}>
      <div className={styles.header}>
        <span className={styles.icon}>{config.icon}</span>
        <span className={styles.title}>{displayTitle}</span>
      </div>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
}
