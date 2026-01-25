import React, {PropsWithChildren} from 'react';

type InteractivePlaygroundProps = PropsWithChildren<{
  language?: string;
}>;

export function InteractivePlayground({
  language = 'text',
  children,
}: InteractivePlaygroundProps) {
  return (
    <div className="interactive-playground">
      <div className="interactive-playground__header">
        <span>Interactive playground</span>
        <span className="interactive-playground__language">{language}</span>
      </div>
      <div className="interactive-playground__body">
        {children || <span>Interactive version coming soon.</span>}
      </div>
    </div>
  );
}
