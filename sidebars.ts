import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Observability',
      link: {
        type: 'generated-index',
        title: 'Observability',
        description: 'Enterprise-grade observability practices: distributed tracing, metrics collection, log aggregation, and the OpenTelemetry ecosystem.',
        slug: '/observability',
      },
      items: [
        'observability/introduction',
        'observability/three-pillars',
        'observability/opentelemetry',
        {
          type: 'category',
          label: 'Language Integrations',
          link: {
            type: 'doc',
            id: 'observability/integrations/overview',
          },
          items: [
            'observability/integrations/go',
            'observability/integrations/dotnet',
            'observability/integrations/nodejs',
            'observability/integrations/python',
            'observability/integrations/java',
          ],
        },
        'observability/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Infrastructure & CI/CD',
      link: {
        type: 'generated-index',
        title: 'Infrastructure & CI/CD',
        description: 'Kubernetes deployment patterns, CI/CD pipeline architectures, and infrastructure best practices.',
        slug: '/infrastructure',
      },
      items: [
        'infrastructure/kubernetes-basics',
        'infrastructure/ci-cd-patterns',
      ],
    },
    {
      type: 'category',
      label: 'Development',
      link: {
        type: 'generated-index',
        title: 'Development',
        description: 'Modern development practices, API design principles, and language-specific patterns.',
        slug: '/development',
      },
      items: [
        'development/api-design',
        'development/react-patterns',
        'development/typescript-tips',
      ],
    },
    {
      type: 'category',
      label: 'Best Practices',
      link: {
        type: 'generated-index',
        title: 'Best Practices',
        description: 'Code review guidelines, testing strategies, and documentation standards.',
        slug: '/best-practices',
      },
      items: [
        'best-practices/code-review',
        'best-practices/testing-strategies',
        'best-practices/documentation',
      ],
    },
  ],
};

export default sidebars;
