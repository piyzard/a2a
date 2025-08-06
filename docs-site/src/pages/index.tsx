import type {ReactNode} from 'react';
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
          KubeStellar A2A Agent
        </Heading>
        <p className={styles.heroSubtitle}>
          Think of KubeStellar A2A as an <strong>intelligent orchestrator</strong> for your multi-cluster Kubernetes operations - seamlessly managing workloads across clusters with AI-powered automation and natural language interfaces.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/getting-started/">
            Documentation
          </Link>
          <Link
            className="button button--primary button--lg"
            href="https://github.com/kubestellar/a2a">
            Join Us on GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

function HowItWorks() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <div className="text--center">
              <Heading as="h2">How it Works</Heading>
              <p className="hero__subtitle">
                KubeStellar A2A provides a unified platform for multi-cluster Kubernetes management with intelligent automation
              </p>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <Heading as="h3">🤖 AI-Powered Interface</Heading>
              <p>
                Natural language processing for Kubernetes operations. Describe what you want, and let AI handle the complexity.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <Heading as="h3">🌐 Multi-Cluster Native</Heading>
              <p>
                Seamlessly manage resources across multiple Kubernetes clusters with advanced targeting and policy enforcement.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <Heading as="h3">⚙️ KubeStellar Integration</Heading>
              <p>
                Full support for KubeStellar 2024 architecture with WDS, ITS, and binding policies for workload placement.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function KeyFeatures() {
  const features = [
    '✓ Dual Interface: CLI and AI-powered natural language',
    '✓ Advanced Helm deployments with binding policies', 
    '✓ Multi-namespace operations and resource discovery',
    '✓ Interactive agent mode for conversational management',
    '✓ Complete GVRC discovery across cluster topology',
    '✓ Production-ready with 60+ comprehensive tests',
    '✓ Type-safe with full schema validation',
    '✓ Extensible architecture for custom functions'
  ];

  return (
    <section className={styles.keyFeatures}>
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <Heading as="h2">Key Features</Heading>
            <p>
              KubeStellar A2A revolutionizes how you interact with Kubernetes clusters, providing both programmatic control and intelligent automation in a single platform.
            </p>
            <ul className={styles.featureList}>
              {features.map((feature, idx) => (
                <li key={idx}>{feature}</li>
              ))}
            </ul>
          </div>
          <div className="col col--6">
            <div className={styles.codeExample}>
              <h4>Quick Example</h4>
              <pre><code>{`# Deploy with natural language
uv run kubestellar agent
> "Deploy nginx to all production clusters with high availability"

# Or use direct CLI commands
uv run kubestellar execute helm_deploy \\
  -P chart_name=nginx \\
  -P target_clusters='["prod-us", "prod-eu"]' \\
  -P create_binding_policy=true

# AI-powered cluster analysis
> "Show me cluster health and resource distribution"`}</code></pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function GetStarted() {
  return (
    <section className={styles.getStarted}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <div className="text--center">
              <Heading as="h2">Get Started in Minutes</Heading>
              <p>
                Install KubeStellar A2A and transform your Kubernetes management experience
              </p>
              <div className={styles.startButtons}>
                <Link
                  className="button button--primary button--lg margin--sm"
                  to="/docs/getting-started/installation">
                  Install Now
                </Link>
                <Link
                  className="button button--secondary button--lg margin--sm"
                  to="/docs/getting-started/quick-start">
                  5-Minute Tutorial
                </Link>
                <Link
                  className="button button--outline button--lg margin--sm"
                  href="https://github.com/kubestellar/a2a">
                  View on GitHub
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="KubeStellar A2A - AI-Powered Multi-Cluster Kubernetes Management"
      description="Advanced multi-cluster Kubernetes management with AI-powered automation, natural language interfaces, and seamless KubeStellar integration.">
      <HomepageHeader />
      <main>
        <HowItWorks />
        <KeyFeatures />
        <GetStarted />
      </main>
    </Layout>
  );
}
