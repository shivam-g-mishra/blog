import React from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import styles from './LanguageSelector.module.css';

type Language = {
  value: string;
  label: string;
  icon: string;
};

const LANGUAGES: Language[] = [
  { value: 'python', label: 'Python', icon: '🐍' },
  { value: 'typescript', label: 'TypeScript', icon: '📘' },
  { value: 'go', label: 'Go', icon: '🔵' },
  { value: 'java', label: 'Java', icon: '☕' },
  { value: 'cpp', label: 'C++', icon: '⚡' },
  { value: 'c', label: 'C', icon: '🔧' },
  { value: 'csharp', label: 'C#', icon: '💜' },
];

type LanguageSelectorProps = {
  defaultValue?: string;
};

/**
 * Language selector that appears at the top of interview guide pages.
 * Selection syncs with all CodeTabs on the page via groupId="language".
 */
export function LanguageSelector({ defaultValue = 'python' }: LanguageSelectorProps) {
  return (
    <div className={styles.languageSelector}>
      <div className={styles.header}>
        <span className={styles.label}>Select your preferred language:</span>
      </div>
      <Tabs
        defaultValue={defaultValue}
        groupId="language"
        className={styles.tabs}
      >
        {LANGUAGES.map((lang) => (
          <TabItem
            key={lang.value}
            value={lang.value}
            label={`${lang.icon} ${lang.label}`}
            className={styles.tabItem}
          >
            <div className={styles.selectedMessage}>
              All code examples below will display in <strong>{lang.label}</strong>
            </div>
          </TabItem>
        ))}
      </Tabs>
    </div>
  );
}

export { LANGUAGES };
export type { Language };
