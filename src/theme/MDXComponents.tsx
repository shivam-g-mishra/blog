import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {
  PatternMeta,
  Difficulty,
  TimeToRead,
  Prerequisites,
} from '@site/src/components/design-patterns/PatternMeta';
import {InteractivePlayground} from '@site/src/components/design-patterns/InteractivePlayground';
import {CodeTabs} from '@site/src/components/design-patterns/CodeTabs';

export default {
  ...MDXComponents,
  PatternMeta,
  Difficulty,
  TimeToRead,
  Prerequisites,
  InteractivePlayground,
  CodeTabs,
  Tabs,
  TabItem,
};
