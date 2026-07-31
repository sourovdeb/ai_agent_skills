/**
 * SMART EMAIL COMPOSER — Sourov DEB
 * Generates personalised, narrative-informed outreach emails
 * 
 * DEPENDENCIES: Google Drive (file IDs for CV + motivation letter), Gmail
 * NO GOOGLE SHEETS REQUIRED
 * 
 * VERSION: 1.0 | Date: 29 May 2026
 */

// ==================== CONFIGURATION ====================

// REQUIRED: Paste your Google Drive file IDs here
const PDF_CONFIG = {
  CV_FILE_ID: 'YOUR_CV_FILE_ID',              // Find: Share CV PDF, get link, extract ID
  MOTIVATION_FILE_ID: 'YOUR_MOTIVATION_FILE_ID', // Find: Share motivation PDF, get link, extract ID
};

// Email sender metadata
const SENDER = {
  name: 'Sourov DEB',
  email: 'sourovdeb.is@gmail.com',
  phone: '06 93 84 61 68',
  location: 'Saint-Pierre, La Réunion, RE',
  languages: 'English, French, Bengali, +1',
  certifications: 'Cambridge CELTA (2026)',
  availability: 'Immediate',
};

// Core story elements (pulled from narrative)
const NARRATIVE_ASSETS = {
  hardSkills: [
    { skill: 'English Teaching', evidence: 'CELTA-certified, 120+ supervised hours, A1–C2' },
    { skill: 'IELTS/TOEIC Specialisation', evidence: '18 years professional environment, exam prep' },
    { skill: 'Multilingual', evidence: 'Bengali, English, French; lived across 3 continents' },
    { skill: 'Hospitality Excellence', evidence: '18 years management: Star Casino Sydney, Merivale Group' },
    { skill: 'Medical English', evidence: 'Healthcare family context, clinical vocabulary' },
    { skill: 'Aeronautical English', evidence: 'International experience, high-stakes communication' },
  ],
  softSkills: [
    { skill: 'Resilience', evidence: 'Migration (3 continents), addiction recovery, mental health advocacy' },
    { skill: 'Cultural Adaptation', evidence: 'Bangladesh → Australia → France → Réunion' },
    { skill: 'Authentic Engagement', evidence: 'Transparent about neurodiversity, accessible teaching' },
    { skill: 'Self-Directed Learning', evidence: 'YouTube projects, blog writing, continuous upskilling' },
  ],
  differentiators: [
    'Neurodivergent (ADHD, bipolar) educator — unique perspective on diverse learner needs',
    'Lived experience across 4 languages + migration trauma — empathy with language anxiety',
    'Transparent mental health advocate — destigmatizes neurodiversity in professional contexts',
    'YouTube presence + blog platform — can boost centre\'s brand visibility',
  ],
};

// ==================== EMAIL TEMPLATES (Customisable) ====================

const EMAIL_TEMPLATES = {
  // Generic: Formal introduction for government/non-profit/educational institutions
  formal: {
    subject: 'Candidature formateur d\'anglais – Cambridge CELTA – {{ORG_NAME}}',
    body: `Madame, Monsieur,

{{ORG_NAME}} reconnaît l'importance de la formation linguistique pour {{ORG_CONTEXT}}. C'est dans ce cadre que je vous propose ma candidature.

Titulaire de la certification **Cambridge CELTA** (2026), je suis formateur d'anglais spécialisé dans {{SPECIALTY}}. Mon parcours combine {{YEARS}} ans d'expérience professionnelle en environnement anglophone avec une pratique pédagogique supervisée de 120+ heures.

Je maîtrise :
• Enseignement tous niveaux (A1–C2)
• {{SPECIALTY}} adapté à votre contexte
• Approche neurodivergence-inclusive

CV et lettre de motivation joints.
Seriez-vous disposé à m'accorder un entretien pour explorer comment mon profil répond à vos besoins ?

Cordialement,
Sourov DEB · 06 93 84 61 68 · sourovdeb.is@gmail.com`
  },

  // Hospitality: Luxury/service sector focused
  hospitality: {
    subject: 'Candidature formateur anglais hôtellerie — Excellence client — {{ORG_NAME}}',
    body: `Madame, Monsieur,

{{ORG_NAME}} accueille une clientèle internationale exigeante. La formation de vos équipes à l'**anglais d'excellence** est un levier stratégique.

Mon parcours : 18 ans dans l'hôtellerie de luxe à Sydney (Star Casino, Merivale Group), certification **Cambridge CELTA**, spécialisation **Business English** et codes culturels anglo-saxons. Je ne forme pas seulement à la langue — je forme aux comportements attendus par les clients VIP.

Modules proposés :
• Anglais opérationnel pour personnel au sol
• Communication VIP + gestion client difficile
• Mise en place protocoles service bilingues

Financement CPF/OPCO possible.

CV et lettre de motivation joints.
Un entretien vous permettrait de juger de ma capacité à concevoir un module sur-mesure.

Respectueusement,
Sourov DEB · 06 93 84 61 68 · sourovdeb.is@gmail.com`
  },

  // Medical: Healthcare/clinical angle
  medical: {
    subject: 'Candidature formateur anglais médical — {{ORG_NAME}}',
    body: `Madame, Monsieur,

Avec l'augmentation du tourisme médical à La Réunion, {{ORG_NAME}} bénéficierait de personnels à l'aise en **anglais médical** — accueil patients, communication d'urgence, terminologie clinique.

Formateur certifié **Cambridge CELTA**, je propose des modules d'anglais médical adaptés aux équipes soignantes. Financement OPCO Santé et CPF possible.

Spécialisations :
• Terminologie médicale (urgence, consultation, diagnostic)
• Communication patient (empathie, clarté, documentation)
• Protocoles de sécurité et communication critique

CV et lettre de motivation joints.
Pourriez-vous m'accorder un entretien pour détailler une proposition de formation courte ?

Cordialement,
Sourov DEB · 06 93 84 61 68 · sourovdeb.is@gmail.com`
  },

  // Education: Schools/training centres/youth
  education: {
    subject: 'Candidature formateur anglais — {{ORG_NAME}}',
    body: `Madame, Monsieur,

{{ORG_NAME}} prépare les jeunes apprenants à une carrière multilingue. C'est dans ce contexte que je soumets ma candidature.

Certifié **Cambridge CELTA** et expérimenté en enseignement primaire (La Réunion, 2024–2025), je maîtrise les méthodes adaptées aux jeunes publics — approche ludique, rituels, éveil linguistique. Natif anglophone, j'adapte tous les niveaux A1–C2.

Spécialisations :
• English for young learners (8–14 ans)
• Préparation examens Cambridge YLE
• Approche neurodivergence-inclusive

CV et lettre de motivation joints.
Un entretien vous permettrait de vérifier mon adéquation avec vos méthodes.

Respectueusement,
Sourov DEB · 06 93 84 61 68 · sourovdeb.is@gmail.com`
  },

  // Aviation/Aeronautical: Airline/aviation sector
  aviation: {
    subject: 'Candidature formateur anglais aéronautique — {{ORG_NAME}}',
    body: `Madame, Monsieur,

{{ORG_NAME}} opère des liaisons où l'anglais est compétence clé pour équipages et personnel. Je propose un profil de formateur spécialisé.

Certifié **Cambridge CELTA**, je maîtrise l'**anglais aéronautique** — vocabulaire de bord, sécurité, relation client en vol — combiné à 18 ans d'expérience en management en environnements exigeants (casino 5 étoiles, restauration gastronomique, Australie).

Modules proposés :
• Anglais aéronautique opérationnel
• Communication équipage – protocoles de sécurité
• Service client en vol – bilingue excellence

Formation finançable CPF et OPCO.

CV et lettre de motivation joints.
Seriez-vous ouvert à un entretien pour maquette de formation « Anglais pour personnels navigants » ?

Bien cordialement,
Sourov DEB · 06 93 84 61 68 · sourovdeb.is@gmail.com`
  },
};

// ==================== ORGANISATION DATABASE ====================

const ORGANISATIONS = [
  {
    name: 'DP LANGUES',
    category: 'language_centre',
    email: 'contact@dplangues.re',
    context: 'des cours d\'anglais en entreprise et en centre',
    specialty: 'Anglais opérationnel (adultes en entreprise)',
    template: 'formal',
  },
  {
    name: 'Les Petits Bilingues',
    category: 'education',
    email: 'contact@lespetitsbilingues.re',
    context: 'des ateliers d\'anglais pour enfants',
    specialty: 'Anglais pour jeunes publics',
    template: 'education',
  },
  {
    name: 'English World',
    category: 'language_centre',
    email: 'contact@englishworld.re',
    context: 'des cours d\'anglais général et professionnel',
    specialty: 'Anglais tous niveaux (A1–C2)',
    template: 'formal',
  },
  {
    name: 'Air Austral',
    category: 'aviation',
    email: 'saintpierre@air-austral.com',
    context: 'des liaisons internationales où l\'anglais est clé',
    specialty: 'Anglais aéronautique',
    template: 'aviation',
  },
  {
    name: 'LUX Resorts',
    category: 'hospitality',
    email: 'luxiledelareunion@luxresorts.com',
    context: 'une clientèle internationale exigeante',
    specialty: 'Anglais hôtellerie excellence',
    template: 'hospitality',
  },
  {
    name: 'Clinique Saint-Vincent',
    category: 'medical',
    email: 'karine.sababadichetty@clinifutur.net',
    context: 'le tourisme médical en hausse',
    specialty: 'Anglais médical',
    template: 'medical',
  },
  {
    name: 'CCI Réunion',
    category: 'government',
    email: 'formation@reunion.cci.fr',
    context: 'des entreprises locales en développement international',
    specialty: 'Business English et négociation',
    template: 'formal',
  },
  {
    name: 'GRETA La Réunion',
    category: 'education',
    email: 'contact@greta-reunion.fr',
    context: 'des parcours de formation pour adultes',
    specialty: 'Anglais tous contextes (CPF/OPCO)',
    template: 'formal',
  },
  {
    name: 'Département 974',
    category: 'government',
    email: 'valerie.fontaine@cg974.fr',
    context: 'la coopération régionale Océan Indien',
    specialty: 'Anglais diplomatique/institutionnel',
    template: 'formal',
  },
  {
    name: 'Région Réunion',
    category: 'government',
    email: 'formation@regionreunion.fr',
    context: 'l\'employabilité et l\'internationalisation',
    specialty: 'Anglais marchés publics/appels d\'offres européens',
    template: 'formal',
  },
  // CONTINUE WITH REMAINING 51 ORGANISATIONS FROM CSV
];

// ==================== CORE FUNCTIONS ====================

function generateEmail(org) {
  if (!EMAIL_TEMPLATES[org.template]) {
    console.error(`❌ Template '${org.template}' not found.`);
    return null;
  }

  let template = EMAIL_TEMPLATES[org.template];
  let subject = template.subject
    .replace('{{ORG_NAME}}', org.name);
  
  let body = template.body
    .replace('{{ORG_NAME}}', org.name)
    .replace('{{ORG_CONTEXT}}', org.context)
    .replace('{{SPECIALTY}}', org.specialty)
    .replace('{{YEARS}}', '18');

  return { subject, body };
}

function loadAttachments() {
  try {
    const cvBlob = DriveApp.getFileById(PDF_CONFIG.CV_FILE_ID).getBlob();
    const motivBlob = DriveApp.getFileById(PDF_CONFIG.MOTIVATION_FILE_ID).getBlob();
    console.log('✅ Attachments loaded');
    return [cvBlob, motivBlob];
  } catch (err) {
    console.error('❌ Failed to load attachments:', err.message);
    return null;
  }
}

function sendBatch(startIndex = 0, batchSize = 10, testMode = true) {
  console.log(`🚀 Starting batch: START=${startIndex}, SIZE=${batchSize}, TEST=${testMode}`);

  const attachments = loadAttachments();
  if (!attachments) {
    console.error('❌ Cannot proceed without attachments.');
    return;
  }

  const endIndex = Math.min(startIndex + batchSize, ORGANISATIONS.length);
  if (startIndex >= ORGANISATIONS.length) {
    console.error(`❌ startIndex (${startIndex}) exceeds total organisations (${ORGANISATIONS.length})`);
    return;
  }

  console.log(`📧 Sending ${endIndex - startIndex} emails...`);

  for (let i = startIndex; i < endIndex; i++) {
    const org = ORGANISATIONS[i];
    const emailData = generateEmail(org);

    if (!emailData) {
      console.error(`⚠️ Skipped ${org.name} — template error`);
      continue;
    }

    let recipient = testMode ? SENDER.email : org.email;

    try {
      GmailApp.sendEmail(recipient, emailData.subject, emailData.body, {
        attachments: attachments,
        name: SENDER.name,
      });
      console.log(`✅ Sent ${i + 1}/${ORGANISATIONS.length} to ${org.name} (${org.email})`);
    } catch (err) {
      console.error(`❌ Failed on ${org.name}: ${err.message}`);
    }

    Utilities.sleep(2000);
  }

  console.log('🎉 Batch complete.');
}

function previewEmail(index = 0) {
  if (index >= ORGANISATIONS.length || index < 0) {
    console.error(`❌ Invalid index. Total organisations: ${ORGANISATIONS.length}`);
    return;
  }

  const org = ORGANISATIONS[index];
  const emailData = generateEmail(org);

  console.log(`\n========== PREVIEW: ${org.name} ==========`);
  console.log(`TO: ${org.email}`);
  console.log(`SUBJECT: ${emailData.subject}`);
  console.log(`\n${emailData.body}`);
  console.log(`\nATTACHMENTS: CV + Motivation Letter`);
  console.log(`==========================================\n`);
}

function exportData() {
  const data = ORGANISATIONS.map((org, idx) => ({
    index: idx,
    name: org.name,
    email: org.email,
    category: org.category,
    specialty: org.specialty,
    template: org.template,
    emailPreview: generateEmail(org),
  }));

  const json = JSON.stringify(data, null, 2);
  console.log(json);
  return json;
}

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Smart Email Composer')
    .addItem('Preview Email (Org 0)', 'previewEmail')
    .addItem('Send Test Batch (5 emails)', 'sendTestBatch')
    .addItem('Export Data', 'exportData')
    .addToUi();
}

function sendTestBatch() {
  sendBatch(0, 5, true);
}
