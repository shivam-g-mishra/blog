import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p className={styles.heroDescription}>
          Senior Software Engineer at NVIDIA with 9+ years of experience building 
          scalable web applications, CI/CD platforms, and observability systems. 
          Sharing insights from production systems serving thousands of developers.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/blog">
            Read the Blog
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/docs/intro">
            Browse Docs
          </Link>
        </div>
      </div>
    </header>
  );
}

type FeatureItem = {
  title: string;
  emoji: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Infrastructure & DevOps',
    emoji: '🏗️',
    description: (
      <>
        Deep dives into Kubernetes, CI/CD pipelines, GitOps, Docker optimization,
        and building scalable infrastructure that handles millions of requests.
      </>
    ),
  },
  {
    title: 'Full-Stack Development',
    emoji: '💻',
    description: (
      <>
        React patterns, TypeScript best practices, Node.js scalability,
        API design, and building real-time analytics dashboards.
      </>
    ),
  },
  {
    title: 'Observability & Monitoring',
    emoji: '📊',
    description: (
      <>
        Production-ready monitoring with Prometheus, Grafana, ELK stack,
        distributed tracing, and alerting strategies that scale.
      </>
    ),
  },
];

function Feature({title, emoji, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <span className={styles.featureEmoji}>{emoji}</span>
        <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Technical Blog - Observability, DevOps & Distributed Systems"
      description="Technical blog by Shivam Mishra, Senior Software Engineer at NVIDIA. In-depth guides on OpenTelemetry, Kubernetes, distributed tracing, Prometheus, Grafana, and building scalable production systems.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
