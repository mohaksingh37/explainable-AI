"""
Case Database
=============
Contains sample legal cases ranging from easy (clear-cut) to difficult (ambiguous).
Each case includes real-world-style narratives for better understanding.
"""

FEATURE_DESCRIPTIONS = {
    'evidence_strength':        {'label': 'Evidence Strength',        'desc': 'How strong is the physical/digital evidence? (0=None, 10=Irrefutable)',          'min': 0,  'max': 10,  'step': 0.5,  'type': 'range'},
    'witness_count':            {'label': 'Number of Witnesses',       'desc': 'Number of credible witnesses testifying',                                        'min': 0,  'max': 10,  'step': 1,    'type': 'range'},
    'prior_criminal_record':    {'label': 'Prior Criminal Record',     'desc': 'Does the defendant have a previous criminal conviction?',                         'min': 0,  'max': 1,   'step': 1,    'type': 'toggle'},
    'legal_representation':     {'label': 'Legal Representation',      'desc': 'Quality of legal representation (0=None, 1=Public Defender, 2=Private Attorney)', 'min': 0,  'max': 2,   'step': 1,    'type': 'select', 'options': ['No Representation', 'Public Defender', 'Private Attorney']},
    'crime_severity':           {'label': 'Crime Severity',            'desc': 'How serious is the alleged crime? (1=Minor Misdemeanor, 5=Felony)',               'min': 1,  'max': 5,   'step': 1,    'type': 'range'},
    'evidence_tampering':       {'label': 'Evidence Tampering',        'desc': 'Was any evidence tampered with or found inadmissible?',                           'min': 0,  'max': 1,   'step': 1,    'type': 'toggle'},
    'defendant_cooperation':    {'label': 'Defendant Cooperation',     'desc': 'Level of defendant cooperation with authorities (0=None, 10=Full)',               'min': 0,  'max': 10,  'step': 0.5,  'type': 'range'},
    'jurisdiction_strictness':  {'label': 'Jurisdiction Strictness',   'desc': 'How strict is the local court jurisdiction? (1=Lenient, 5=Very Strict)',          'min': 1,  'max': 5,   'step': 1,    'type': 'range'},
    'case_media_coverage':      {'label': 'High Media Coverage',       'desc': 'Is the case under significant public/media scrutiny?',                            'min': 0,  'max': 1,   'step': 1,    'type': 'toggle'},
    'time_to_trial_months':     {'label': 'Time to Trial (Months)',    'desc': 'How many months from arrest to trial?',                                           'min': 1,  'max': 36,  'step': 1,    'type': 'range'},
}

# ─── Sample Cases ────────────────────────────────────────────────────────────
SAMPLE_CASES = [
    # ── EASY CASES ──────────────────────────────────────────────────────────
    {
        'id': 0,
        'title': 'The Convenience Store Robbery',
        'difficulty': 'Easy',
        'category': 'Theft / Robbery',
        'narrative': (
            'Rajan Kumar was caught on crystal-clear CCTV footage robbing a convenience store. '
            'Four eyewitnesses, including the store owner and two customers, positively identified him. '
            'He had two prior robbery convictions on his record. His court-appointed public defender '
            'advised him to cooperate, but he refused. The stolen goods were recovered from his home. '
            'The local jurisdiction is known for strict sentencing of repeat offenders.'
        ),
        'expected_outcome': 'Convicted',
        'why': 'Strong CCTV evidence + multiple witnesses + prior record = overwhelming case for prosecution.',
        'features': {
            'evidence_strength': 9.5,
            'witness_count': 4,
            'prior_criminal_record': 1,
            'legal_representation': 1,
            'crime_severity': 3,
            'evidence_tampering': 0,
            'defendant_cooperation': 1.0,
            'jurisdiction_strictness': 4,
            'case_media_coverage': 0,
            'time_to_trial_months': 4
        }
    },
    {
        'id': 1,
        'title': 'The Wrongful Parking Ticket Dispute',
        'difficulty': 'Easy',
        'category': 'Civil Infraction',
        'narrative': (
            'Priya Sharma is fighting a parking ticket. She has GPS logs, a timestamped receipt '
            'from a nearby restaurant proving she was elsewhere, and a reliable witness (her colleague). '
            'She hired a private attorney. She has no prior violations. The evidence clearly shows '
            'she was not at the location during the alleged offence time. The case is in a minor '
            'civil court with no media attention.'
        ),
        'expected_outcome': 'Acquitted',
        'why': 'Clear alibi evidence, credible witness, good legal representation, minor offence.',
        'features': {
            'evidence_strength': 8.5,
            'witness_count': 1,
            'prior_criminal_record': 0,
            'legal_representation': 2,
            'crime_severity': 1,
            'evidence_tampering': 0,
            'defendant_cooperation': 9.0,
            'jurisdiction_strictness': 1,
            'case_media_coverage': 0,
            'time_to_trial_months': 2
        }
    },

    # ── MEDIUM CASES ─────────────────────────────────────────────────────────
    {
        'id': 2,
        'title': 'The Corporate Embezzlement',
        'difficulty': 'Medium',
        'category': 'White-Collar Crime / Fraud',
        'narrative': (
            'CFO Arvind Mehta is accused of siphoning ₹2 crore from his company over 3 years. '
            'Forensic accountants found irregularities in financial records. However, the defence '
            'argues the transactions were authorized. Two witnesses corroborate the company\'s version, '
            'but Arvind\'s high-profile private attorney found procedural errors in how evidence was obtained. '
            'The case has significant media coverage. Arvind has no prior criminal record and has been '
            'fully cooperative. The trial took 18 months to begin.'
        ),
        'expected_outcome': 'Uncertain',
        'why': 'Evidence tampering issues weaken prosecution; good lawyer + cooperation + clean record help defence.',
        'features': {
            'evidence_strength': 6.5,
            'witness_count': 2,
            'prior_criminal_record': 0,
            'legal_representation': 2,
            'crime_severity': 4,
            'evidence_tampering': 1,
            'defendant_cooperation': 8.0,
            'jurisdiction_strictness': 3,
            'case_media_coverage': 1,
            'time_to_trial_months': 18
        }
    },
    {
        'id': 3,
        'title': 'The Campus Drug Possession',
        'difficulty': 'Medium',
        'category': 'Drug Offense',
        'narrative': (
            'College student Rahul Desai was found with a small quantity of marijuana during a '
            'routine hostel check. A single security guard is the only witness. Rahul claims the '
            'substance was planted. He has no prior criminal record and immediately cooperated '
            'with authorities. His parents hired a competent private attorney. The college is in '
            'a state with moderate drug laws. The case has drawn minor local media attention. '
            'Trial is set 8 months after the incident.'
        ),
        'expected_outcome': 'Likely Acquitted',
        'why': 'Single witness, cooperation, clean record, and good legal representation balance out the prosecution.',
        'features': {
            'evidence_strength': 4.0,
            'witness_count': 1,
            'prior_criminal_record': 0,
            'legal_representation': 2,
            'crime_severity': 2,
            'evidence_tampering': 0,
            'defendant_cooperation': 9.5,
            'jurisdiction_strictness': 2,
            'case_media_coverage': 0,
            'time_to_trial_months': 8
        }
    },

    # ── HARD / COMPLEX CASES ─────────────────────────────────────────────────
    {
        'id': 4,
        'title': 'The High-Profile Murder Trial',
        'difficulty': 'Hard',
        'category': 'Homicide',
        'narrative': (
            'Former politician Suresh Rao is accused of ordering the assassination of a journalist. '
            'The case has dominated national news for months. While physical evidence at the scene '
            'is strong, a key witness retracted their statement under alleged pressure. '
            'The defence team, one of India\'s most expensive law firms, found chain-of-custody '
            'issues with crucial forensic evidence. Rao has no prior criminal record and has '
            'maintained a composed, cooperative demeanour throughout. The jurisdiction — a major '
            'metropolitan High Court — is known for rigorous scrutiny. Trial began 24 months after arrest.'
        ),
        'expected_outcome': 'Uncertain — contested evidence and elite defence make this unpredictable.',
        'why': 'High severity + media pressure vs. evidence tampering issues + elite legal team + clean record.',
        'features': {
            'evidence_strength': 7.0,
            'witness_count': 1,
            'prior_criminal_record': 0,
            'legal_representation': 2,
            'crime_severity': 5,
            'evidence_tampering': 1,
            'defendant_cooperation': 7.0,
            'jurisdiction_strictness': 5,
            'case_media_coverage': 1,
            'time_to_trial_months': 24
        }
    },
    {
        'id': 5,
        'title': 'The Cybercrime Identity Theft',
        'difficulty': 'Hard',
        'category': 'Cybercrime / Identity Theft',
        'narrative': (
            'Tech professional Neha Kulkarni is accused of stealing identities of 200 bank customers '
            'using a phishing kit she allegedly deployed. Digital forensics link her IP address to '
            'the attack, but her attorney argues the IP was spoofed and no direct fingerprint ties '
            'her to the malware. Seven bank officials testified about financial losses. '
            'Neha has one prior conviction for software piracy 6 years ago. '
            'She partially cooperated but refused to hand over her personal laptop. '
            'The case is in a strict cyber-crime court. Trial was delayed by 14 months due to '
            'complexity of evidence.'
        ),
        'expected_outcome': 'Likely Convicted',
        'why': 'Multiple witnesses, prior record, refusal to cooperate fully, and strict jurisdiction weigh heavily.',
        'features': {
            'evidence_strength': 6.0,
            'witness_count': 7,
            'prior_criminal_record': 1,
            'legal_representation': 2,
            'crime_severity': 4,
            'evidence_tampering': 0,
            'defendant_cooperation': 4.0,
            'jurisdiction_strictness': 5,
            'case_media_coverage': 1,
            'time_to_trial_months': 14
        }
    },
    {
        'id': 6,
        'title': 'The Domestic Violence Allegation',
        'difficulty': 'Hard',
        'category': 'Assault / Domestic Violence',
        'narrative': (
            'Businessman Vikram Joshi is accused of repeated domestic violence by his spouse. '
            'Medical reports show injuries consistent with assault. However, Vikram claims the '
            'injuries were accidental. A neighbour witnessed a physical altercation. '
            'Vikram\'s private attorney argues that the police failed to properly document the '
            'scene, raising chain-of-custody questions. Vikram has no prior criminal record and '
            'appeared cooperative in court but refused a polygraph. '
            'The case is in a moderate jurisdiction. The case received no media attention.'
        ),
        'expected_outcome': 'Uncertain — medical evidence vs procedural flaws.',
        'why': 'Medical evidence supports prosecution; procedural errors and no prior record complicate the outcome.',
        'features': {
            'evidence_strength': 6.5,
            'witness_count': 1,
            'prior_criminal_record': 0,
            'legal_representation': 2,
            'crime_severity': 3,
            'evidence_tampering': 1,
            'defendant_cooperation': 5.0,
            'jurisdiction_strictness': 3,
            'case_media_coverage': 0,
            'time_to_trial_months': 10
        }
    },
    {
        'id': 7,
        'title': 'The Environmental Pollution Case',
        'difficulty': 'Hard',
        'category': 'Environmental Crime / Corporate',
        'narrative': (
            'Chandra Chemical Industries is accused of illegally dumping toxic waste in a river, '
            'affecting three villages. Environmental agency reports confirm pollution levels. '
            'Satellite imagery and water tests serve as evidence. Twelve villagers testified about '
            'health impacts. However, the company\'s legal team (top-tier environmental lawyers) '
            'argue the pollution pre-existed and the methodology of testing was flawed. '
            'The company has two prior environmental violations. The CEO shows no remorse and '
            'has stonewalled investigators. Heavy media and NGO attention. Trial after 20 months.'
        ),
        'expected_outcome': 'Likely Convicted',
        'why': 'Multiple witnesses, satellite evidence, prior record, non-cooperation, and media pressure.',
        'features': {
            'evidence_strength': 7.5,
            'witness_count': 10,
            'prior_criminal_record': 1,
            'legal_representation': 2,
            'crime_severity': 4,
            'evidence_tampering': 0,
            'defendant_cooperation': 1.0,
            'jurisdiction_strictness': 4,
            'case_media_coverage': 1,
            'time_to_trial_months': 20
        }
    }
]
