import React, {PropsWithChildren} from 'react';
import Tabs from '@theme/Tabs';

type CodeTabsProps = PropsWithChildren<{
  defaultValue?: string;
  groupId?: string;
}>;

export function CodeTabs({
  defaultValue = 'python',
  groupId = 'language',
  children,
}: CodeTabsProps) {
  return (
    <Tabs defaultValue={defaultValue} groupId={groupId}>
      {children}
    </Tabs>
  );
}
