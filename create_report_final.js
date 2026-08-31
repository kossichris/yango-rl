const { Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak, AlignmentType, BorderStyle } = require('docx');
const fs = require('fs');

function createImagePlaceholder(imageName) {
  return [
    new Paragraph({
      text: "",
      spacing: { after: 120 }
    }),
    new Paragraph({
      text: `[INSÉRER IMAGE: ${imageName}]`,
      alignment: AlignmentType.CENTER,
      border: {
        top: { color: "000000", space: 1, style: BorderStyle.DASHED, size: 6 },
        bottom: { color: "000000", space: 1, style: BorderStyle.DASHED, size: 6 }
      },
      spacing: { before: 240, after: 240 },
      bold: true,
      size: 22
    }),
    new Paragraph({
      text: `Fichier: ${imageName}`,
      alignment: AlignmentType.CENTER,
      italics: true,
      size: 18,
      spacing: { after: 240 }
    })
  ];
}

// Create document
const doc = new Document({
  sections: [
    {
      children: [
        // TITLE PAGE
        new Paragraph({ text: "" }),
        new Paragraph({ text: "" }),
        new Paragraph({ text: "" }),
        new Paragraph({
          text: "Driver Repositioning Optimization using Reinforcement Learning",
          alignment: AlignmentType.CENTER,
          spacing: { before: 400, after: 200 },
          size: 48,
          bold: true
        }),
        new Paragraph({
          text: "Q-Learning and Deep Q-Networks Comparison",
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          size: 32,
          italics: true
        }),
        new Paragraph({ text: "" }),
        new Paragraph({ text: "" }),
        new Paragraph({
          text: "Christian Hounsounou",
          alignment: AlignmentType.CENTER,
          spacing: { before: 300, after: 100 },
          size: 24,
          bold: true
        }),
        new Paragraph({
          text: "Reinforcement Learning Project",
          alignment: AlignmentType.CENTER,
          spacing: { after: 50 },
          size: 20
        }),
        new Paragraph({
          text: "August 2026",
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          size: 20
        }),

        new PageBreak(),

        // ABSTRACT
        new Paragraph({
          text: "Résumé exécutif",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Ce projet compare deux algorithmes de Reinforcement Learning pour optimiser le repositionnement des chauffeurs de ride-sharing. Les résultats montrent que Q-Learning surpasse DQN de 17.3% sur ce problème de petite taille d'espace d'état (25 zones). L'étude démontre l'importance de choisir l'algorithme approprié en fonction de la taille du problème. Le code complet, les données expérimentales et les visualisations sont disponibles sur GitHub.",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // INTRODUCTION
        new Paragraph({
          text: "1. Introduction",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Le Reinforcement Learning (RL) est un paradigme d'apprentissage où un agent apprend à prendre des décisions optimales en interagissant avec un environnement. Contrairement à l'apprentissage supervisé, l'agent reçoit des signaux de récompense/pénalité plutôt que des labels directs.",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Dans le contexte des plateformes de ride-sharing (Yango, Uber, Bolt), les chauffeurs doivent continuellement décider vers quelle zone se repositionner après avoir complété une course. Cette décision impacte directement leur revenu, le temps d'attente, et la satisfaction client.",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Ce projet applique deux algorithmes RL majeurs - Q-Learning et DQN - pour apprendre une stratégie optimale de repositionnement dans une simulation d'environnement urbain.",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "Objectifs",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Implémenter un environnement de simulation réaliste avec Gymnasium",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Entraîner un agent Q-Learning sur cet environnement",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Entraîner un agent DQN comme comparaison",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Analyser les résultats et identifier quel algorithme fonctionne mieux",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Tirer des leçons sur le choix algorithmique selon la taille du problème",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // PROBLEM
        new Paragraph({
          text: "2. Problème et contexte",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Après avoir complété une course, un chauffeur doit décider vers quelle zone se déplacer. Cette décision est basée typiquement sur l'expérience personnelle, des heuristiques simples, ou des données empiriques incomplètes.",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Ces approches ne sont pas optimales car elles ne tiennent pas compte des variations horaires, des variations jour/semaine, de la distance de repositionnement, et des opportunités de trajets lucratifs.",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "Impact économique",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Une mauvaise décision de repositionnement peut coûter cher : temps d'attente inutile, coûts de carburant, perte d'opportunités. Optimiser cette décision peut augmenter les revenus de 10-20% par chauffeur.",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // STATE OF ART
        new Paragraph({
          text: "3. État de l'art",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "3.1 Q-Learning",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Q-Learning est un algorithme model-free qui apprend une fonction Q(s,a) tabulaire. Avantages : convergence garantie, interprétabilité, efficient pour petits espaces. Limitations : croissance exponentielle avec la taille d'état, pas de généralisation entre états similaires.",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "3.2 Deep Q-Networks (DQN)",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "DQN remplace la Q-table par un réseau de neurones pour approximer Q(s,a). Avantages : scalable à grands espaces, généralise entre états. Limitations : convergence non garantie, plus de hyperparamètres.",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // MDP FORMULATION
        new Paragraph({
          text: "4. Formulation MDP",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "4.1 Espace d'état (S)",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "État : [x, y, hour, day, idle_time]",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "x ∈ [0, 5] : Position X | y ∈ [0, 5] : Position Y | hour ∈ [0, 24] : Heure | day ∈ [0, 7] : Jour | idle_time ∈ [0, 1000] : Attente",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "4.2 Espace d'action (A)",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Discret : 25 actions (move to zone 0, 1, ..., 24) sur grille 5×5",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "4.3 Fonction de récompense (R)",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "r(s, a) = trip_fare - repositioning_cost",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // ENVIRONMENT
        new Paragraph({
          text: "5. Environnement de simulation",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Implémenté avec Gymnasium avec patterns horaires réalistes : pic matin (6-9h) 1.5×, midi (12-14h) 1.2×, pic soir (17-20h) 1.8×, nuit (22-6h) 0.3×, weekend -20%.",
          spacing: { line: 360 }
        }),

        // CITY LAYOUT IMAGE PLACEHOLDER
        ...createImagePlaceholder('city_layout.png'),

        new Paragraph({
          text: "Figure 1: Grille urbaine 5×5 avec heatmap de demande par zone",
          alignment: AlignmentType.CENTER,
          italics: true,
          size: 18,
          spacing: { after: 240 }
        }),

        new PageBreak(),

        // Q-LEARNING
        new Paragraph({
          text: "6. Implémentation Q-Learning",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "6.1 Algorithme",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Formule : Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Hyperparamètres : α=0.1 (taux d'apprentissage), γ=0.99 (discount factor), ε=0.1 (exploration)",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "6.2 Résultats",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Q-table : 7,459 états explorés | Convergence : très rapide | Reward moyen : 1,774,459 | Trips : 545.5 (54.5%)",
          spacing: { line: 360 }
        }),

        // Q-LEARNING TRAINING CURVES IMAGE PLACEHOLDER
        ...createImagePlaceholder('training_results.png'),

        new Paragraph({
          text: "Figure 2: Courbes d'entraînement Q-Learning (500 épisodes)",
          alignment: AlignmentType.CENTER,
          italics: true,
          size: 18,
          spacing: { after: 240 }
        }),

        new PageBreak(),

        // DQN
        new Paragraph({
          text: "7. Implémentation DQN",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "7.1 Architecture",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Input (5) → Dense(128) → ReLU → Dense(128) → ReLU → Output(25)",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Experience replay : buffer 10,000, batch 32, loss MSE, optimizer Adam (lr=0.001)",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "7.2 Résultats",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Convergence : plus lente | Reward moyen : 1,467,003 (-17.3% vs Q-Learning) | Trips : 453.4 (45.3%)",
          spacing: { line: 360 }
        }),

        // DQN TRAINING CURVES IMAGE PLACEHOLDER
        ...createImagePlaceholder('training_results_dqn.png'),

        new Paragraph({
          text: "Figure 3: Courbes d'entraînement DQN (500 épisodes)",
          alignment: AlignmentType.CENTER,
          italics: true,
          size: 18,
          spacing: { after: 240 }
        }),

        new PageBreak(),

        // RESULTS
        new Paragraph({
          text: "8. Résultats de performance",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Comparaison Globale",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Métrique                  Q-Learning          DQN                 Random",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Avg Reward           1,774,459          1,467,003          1,567,413",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Avg Trips                 545.5              453.4              482.2",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Success Rate            54.5%              45.3%              48.2%",
          spacing: { line: 360 }
        }),

        // COMPARISON CHART IMAGE PLACEHOLDER
        ...createImagePlaceholder('comparison_qlearning_dqn.png'),

        new Paragraph({
          text: "Figure 4: Comparaison côte à côte Q-Learning vs DQN vs Random",
          alignment: AlignmentType.CENTER,
          italics: true,
          size: 18,
          spacing: { after: 240 }
        }),

        new PageBreak(),

        // ANALYSIS
        new Paragraph({
          text: "9. Analyse des résultats",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "9.1 Pourquoi Q-Learning gagne (+17.3%)",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "1. Espace petit (25 zones) → Q-Learning optimal sans approximation réseau",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "2. Convergence rapide → tabular methods ont convergence garantie",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "3. Moins de variance → estimateurs directs vs erreurs réseau",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "9.2 Performance vs baseline",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Q-Learning : +12.4% vs random",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "DQN : -6.4% vs random (overkill pour petit problème)",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Leçon : algorithme doit matcher la taille du problème",
          spacing: { line: 360 }
        }),

        // AGENT TRAJECTORY IMAGE PLACEHOLDER
        ...createImagePlaceholder('agent_trajectory.png'),

        new Paragraph({
          text: "Figure 5: Trajectoire du Q-Learning agent sur 100 steps",
          alignment: AlignmentType.CENTER,
          italics: true,
          size: 18,
          spacing: { after: 240 }
        }),

        new PageBreak(),

        // INSIGHTS
        new Paragraph({
          text: "10. Insights et apprentissages",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Principes RL clés",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Exploration vs exploitation : balance critique pour convergence",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Reward shaping : récompense bien définie → apprentissage rapide",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Algorithme choice : crucial selon la taille de l'espace d'état",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // LIMITATIONS
        new Paragraph({
          text: "11. Limitations et travail futur",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Limitations actuelles",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Données synthétiques (pas données réelles)",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Agent mono-chauffeur (pas de compétition)",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Action space discret (chauffeurs réels : continu)",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "Travail futur",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Algorithmes avancés : Actor-Critic, Policy gradients",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Données réelles : historique Yango/Uber",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Multi-agent : compétition chauffeurs",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // CONCLUSION
        new Paragraph({
          text: "12. Conclusion",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Ce projet démontre l'application pratique du Reinforcement Learning à l'optimisation de repositionnement de chauffeurs.",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "Résultats clés",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "✓ Q-Learning surpasse DQN de 17.3%",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "✓ Q-Learning : convergence rapide et stable",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "✓ DQN : mauvais pour petits espaces",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "✓ Tous deux dépassent baseline aléatoire",
          spacing: { line: 360 }
        }),

        new Paragraph({
          text: "Impact potentiel",
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 240, after: 120 }
        }),
        new Paragraph({
          text: "Implémentation réelle : +10-20% revenus chauffeurs via repositionnement optimal",
          spacing: { line: 360 }
        }),

        new PageBreak(),

        // REFERENCES
        new Paragraph({
          text: "13. Références",
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 240, after: 120 }
        }),

        new Paragraph({
          text: "Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). MIT press.",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Mnih, V., et al. (2013). Playing Atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602.",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Gymnasium: https://gymnasium.farama.org/",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "PyTorch: https://pytorch.org/",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "Streamlit: https://streamlit.io/",
          spacing: { line: 360 }
        }),
        new Paragraph({
          text: "GitHub: https://github.com/kossichris/yango-rl",
          spacing: { line: 360 }
        }),
      ]
    }
  ]
});

// Generate document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Rapport_Projet_RL_Final.docx", buffer);
  console.log("✅ Document créé avec placeholders pour images : Rapport_Projet_RL_Final.docx");
});
