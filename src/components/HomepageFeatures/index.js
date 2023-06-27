import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const random_description = [
(
	<>
		Helm Laya Irama memiliki damage boost terbesar, mencapai 100%. Bahkan armor hercules hanya memiliki 75% damage boost terhadap 1 target spesifik.
	</>
),
(
	<>
		Armor parasite tidak mengaplikasikan stack debuff, tetapi mengaplikasikan debuff berdasarkan level debuff di serangan tersebut. Contoh: jika 2 serangan pertama dari parasite sengaja tidak kena, serangan ke-3 akan memberikan debuff yang setara dengan efek stack ke-3. Ini memiliki mekanisme yang berbeda dari despair dagger.
	</>
),
(
	<>
		Space Trooper adalah hero yang memiliki serangan yang paling tinggi daripada hero lain, mencapai 17.5 damage dalam 1 hit.
	</>
),
(
	<>
		Trace adalah satu satunya hero yang memiliki 4x lompat, sedangkan Skywalker adalah satu satunya hero yang memiliki 3x lompat, namun hero lain rata-rata rata hanya bisa 1x lompat
	</>
),
];

const random = Math.floor(Math.random() * random_description.length);

const FeatureList = [
    // title: 'Focus on What Matters',
    // Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    // description: (
      // <>
        // Docusaurus lets you focus on your docs, and we&apos;ll do the chores. Go
        // ahead and move your docs into the <code>docs</code> directory.
      // </>
    // ),
  // },
  {
    title: 'Random Fact',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: random_description[random]
  },
];

function Feature({Svg, title, description}) {
      // <div className="text--center">
        // <Svg className={styles.featureSvg} role="img" />
      // </div>
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
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
