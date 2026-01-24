import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Shivam Mishra',
  tagline: 'Scalable Systems | DevOps | Full-Stack Engineering',
  favicon: 'img/favicon.svg',

  // Set the production url of your site here
  url: 'https://blog.shivamm.info',
  // Set the /<baseUrl>/ pathname under which your site is served
  // Served at root of the blog subdomain
  baseUrl: '/',

  // GitHub pages deployment config (if you decide to use it)
  organizationName: 'shivam-g-mishra',
  projectName: 'blog',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  
  // SEO: Consistent URL format (no trailing slashes)
  trailingSlash: false,

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // SEO: Additional head tags
  headTags: [
    {
      tagName: 'meta',
      attributes: {
        name: 'author',
        content: 'Shivam Mishra',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'robots',
        content: 'index, follow',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'author',
        href: 'https://shivamm.info',
      },
    },
  ],

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
          trackingID: 'G-GQ4KXN5PG2',
          anonymizeIP: true,
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          filename: 'sitemap.xml',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Social card image (used for Open Graph and Twitter cards)
    image: 'img/social-card.svg',

    // SEO metadata
    metadata: [
      {name: 'keywords', content: 'observability, OpenTelemetry, DevOps, Kubernetes, distributed systems, monitoring, Prometheus, Grafana, distributed tracing, software engineering'},
      {name: 'twitter:card', content: 'summary_large_image'},
      {name: 'twitter:creator', content: '@shivam_g_mishra'},
      {property: 'og:type', content: 'website'},
      {property: 'og:locale', content: 'en_US'},
      {property: 'og:site_name', content: 'Shivam Mishra - Technical Blog'},
    ],
    
    // Announcement bar (optional)
    announcementBar: {
      id: 'welcome',
      content: 'Welcome to my blog! Sharing insights from building scalable systems at NVIDIA.',
      backgroundColor: '#22c55e',
      textColor: '#052e16',
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
          href: 'https://shivamm.info',
          label: 'Home',
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
              label: 'Landing Site',
              href: 'https://shivamm.info',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Shivam Mishra. Senior Software Engineer @ NVIDIA.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.oneDark,
      additionalLanguages: [
        'bash',
        'diff',
        'json',
        'yaml',
        'docker',
        'go',
        'python',
        'java',
        'csharp',
        'typescript',
        'sql',
        'nginx',
        'toml',
        'properties',
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

  // Mermaid diagrams support
  markdown: {
    mermaid: true,
  },
  
  // Themes: Mermaid for diagrams + Local search for SEO and UX
  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        indexBlog: true,
        indexDocs: true,
        blogRouteBasePath: "/blog",
        docsRouteBasePath: "/docs",
        highlightSearchTermsOnTargetPage: true,
        searchBarShortcutHint: true,
        language: ["en"],
      },
    ],
  ],
};

export default config;
