import React from 'react';
import styles from './TimeEstimate.module.css';

type TimeEstimateProps = {
  /** Time to understand the concept (e.g., "30 minutes") */
  learnTime?: string;
  /** Time to practice and get comfortable (e.g., "2-3 hours") */
  practiceTime?: string;
  /** Number of problems to feel confident (e.g., "5-10 problems") */
  masteryTime?: string;
  /** How often this appears in interviews (e.g., "60%") */
  interviewFrequency?: string;
  /** Difficulty range (e.g., "Easy to Medium") */
  difficultyRange?: string;
  /** What you should know first */
  prerequisites?: string;
};

/**
 * Displays time estimates and expectations for a topic.
 * Helps readers plan their study time and set expectations.
 * 
 * Usage:
 * <TimeEstimate 
 *   learnTime="30-45 minutes"
 *   practiceTime="2-3 hours"
 *   masteryTime="5-10 problems"
 *   interviewFrequency="60%"
 *   difficultyRange="Easy to Medium"
 *   prerequisites="Arrays, basic loops"
 * />
 */
export function TimeEstimate({
  learnTime,
  practiceTime,
  masteryTime,
  interviewFrequency,
  difficultyRange,
  prerequisites,
}: TimeEstimateProps) {
  const hasContent = learnTime || practiceTime || masteryTime || interviewFrequency || difficultyRange || prerequisites;
  
  if (!hasContent) return null;
  
  return (
    <div className={styles.container}>
      <h3 className={styles.header}>
        <span className={styles.icon}>⏱️</span>
        What to Expect
      </h3>
      <table className={styles.table}>
        <tbody>
          {learnTime && (
            <tr>
              <td className={styles.label}>Learning time</td>
              <td className={styles.value}>{learnTime}</td>
            </tr>
          )}
          {practiceTime && (
            <tr>
              <td className={styles.label}>Practice time</td>
              <td className={styles.value}>{practiceTime}</td>
            </tr>
          )}
          {masteryTime && (
            <tr>
              <td className={styles.label}>Mastery time</td>
              <td className={styles.value}>{masteryTime}</td>
            </tr>
          )}
          {interviewFrequency && (
            <tr>
              <td className={styles.label}>Interview frequency</td>
              <td className={styles.value}>Asked in ~{interviewFrequency} of coding interviews</td>
            </tr>
          )}
          {difficultyRange && (
            <tr>
              <td className={styles.label}>Difficulty range</td>
              <td className={styles.value}>{difficultyRange}</td>
            </tr>
          )}
          {prerequisites && (
            <tr>
              <td className={styles.label}>Prerequisites</td>
              <td className={styles.value}>{prerequisites}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
