import React, {PropsWithChildren} from 'react';

type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export function PatternMeta({children}: PropsWithChildren) {
  return <div className="pattern-meta">{children}</div>;
}

export function Difficulty({level}: {level: DifficultyLevel}) {
  const label = level.charAt(0).toUpperCase() + level.slice(1);

  return (
    <span className={`pattern-meta__chip pattern-meta__difficulty pattern-meta__difficulty--${level}`}>
      Difficulty: {label}
    </span>
  );
}

export function TimeToRead({minutes}: {minutes: number}) {
  if (!minutes || minutes <= 0) {
    return null;
  }

  return <span className="pattern-meta__chip">Time to read: {minutes} min</span>;
}

export function Prerequisites({patterns = []}: {patterns?: string[]}) {
  if (!patterns.length) {
    return null;
  }

  return (
    <span className="pattern-meta__chip">
      Prerequisites: {patterns.join(', ')}
    </span>
  );
}
