import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Shivam Mishra',
  tagline: 'Scalable Systems | DevOps | Full-Stack Engineering',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://blog.shivam.dev',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config (if you decide to use it)
  organizationName: 'shivam-g-mishra',
  projectName: 'blog',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/shivam-g-mishra/blog/tree/main/',
        },
        blog: {
          showReadingTime: true,
          readingTime: ({content, defaultReadingTime}) =>
            defaultReadingTime({content, options: {wordsPerMinute: 200}}),
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
            copyright: `Copyright © ${new Date().getFullYear()} Shivam Mishra`,
          },
          editUrl: 'https://github.com/shivam-g-mishra/blog/tree/main/',
          blogTitle: 'Shivam\'s Blog',
          blogDescription: 'Insights on scalable systems, DevOps, and software engineering',
          postsPerPage: 10,
          blogSidebarTitle: 'Recent Posts',
          blogSidebarCount: 10,
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          // Add your Google Analytics tracking ID here if you want
          trackingID: 'G-XXXXXXXXXX',
          anonymizeIP: true,
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Social card image
    image: 'img/social-card.jpg',
    
    // Announcement bar (optional)
    announcementBar: {
      id: 'welcome',
      content: 'Welcome to my blog! Sharing insights from building scalable systems at NVIDIA.',
      backgroundColor: '#6366f1',
      textColor: '#ffffff',
      isCloseable: true,
    },

    navbar: {
      title: 'Shivam Mishra',
      logo: {
        alt: 'Shivam Mishra Logo',
        src: 'img/logo.svg',
      },
      items: [
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://shivam.dev',
          label: 'Portfolio',
          position: 'right',
        },
        {
          href: 'https://github.com/shivam-g-mishra',
          label: 'GitHub',
          position: 'right',
        },
        {
          href: 'https://www.linkedin.com/in/shivam-g-mishra',
          label: 'LinkedIn',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Content',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'Docs',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/shivam-g-mishra',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/shivam-g-mishra',
            },
            {
              label: 'Email',
              href: 'mailto:shivam.g.mishra@gmail.com',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Portfolio',
              href: 'https://shivam.dev',
            },
            {
              label: 'RSS Feed',
              to: '/blog/rss.xml',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Shivam Mishra. Senior Software Engineer @ NVIDIA.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: [
        'bash',
        'diff',
        'json',
        'yaml',
        'docker',
        'go',
        'python',
        'java',
        'sql',
        'nginx',
        'toml',
      ],
    },

    // Color mode configuration
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    // Table of contents configuration
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },

    // Algolia search (replace with your own or use local search)
    // algolia: {
    //   appId: 'YOUR_APP_ID',
    //   apiKey: 'YOUR_SEARCH_API_KEY',
    //   indexName: 'YOUR_INDEX_NAME',
    //   contextualSearch: true,
    // },
  } satisfies Preset.ThemeConfig,

  // Add local search plugin (uncomment after npm install)
  // themes: [
  //   [
  //     require.resolve("@easyops-cn/docusaurus-search-local"),
  //     {
  //       hashed: true,
  //       indexBlog: true,
  //       indexDocs: true,
  //       blogRouteBasePath: "/blog",
  //       highlightSearchTermsOnTargetPage: true,
  //     },
  //   ],
  // ],

  // Mermaid diagrams support
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};

export default config;
