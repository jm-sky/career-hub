export const careerEn = {
  career: {
    profile: {
      page: {
        title: 'My Profile',
        subtitle: 'This is what recruiters and your future CVs are built from.',
        save: 'Save',
        error_prefix: 'Failed to load your profile.',
        completeness: 'Profile completeness: {score}%',
      },
      fields: {
        headline: {
          label: 'Headline',
          placeholder: 'e.g. Senior Backend Engineer',
        },
        summary: {
          label: 'Summary',
          placeholder: 'A short overview of your professional background.',
        },
        location: {
          label: 'Location',
          placeholder: 'e.g. Warsaw, Poland',
        },
        visibility: {
          label: 'Visibility',
          options: {
            PRIVATE: 'Private — only you can see this',
            FRIENDS: 'Friends — coming soon, currently same as Private',
            PUBLIC: 'Public — visible to anyone with the link',
          },
        },
        contact: {
          title: 'Contact information',
          subtitle: 'Only shown to you — not included on your public profile page.',
          email: 'Email',
          phone: 'Phone',
          linkedin: 'LinkedIn',
          website: 'Website',
        },
        slug: {
          label: 'Public profile URL',
        },
      },
    },
    publicProfile: {
      page: {
        title: 'Profile',
      },
      not_found: 'This profile does not exist or is not public.',
      error: 'Failed to load this profile.',
    },
    experiences: {
      page: {
        title: 'Experience',
        subtitle: 'Your work history — this feeds every CV you generate.',
        add: 'Add experience',
        empty: 'No experience entries yet. Add your first one.',
        error: 'Failed to load your experience entries.',
      },
      form: {
        createTitle: 'Add experience',
        editTitle: 'Edit experience',
        subtitle: 'Describe a role you held, its dates, and the technologies you used.',
      },
      fields: {
        companyName: 'Company',
        position: 'Position',
        employmentType: 'Employment type',
        employmentTypePlaceholder: 'e.g. full_time, contract, freelance',
        startDate: 'Start date',
        endDate: 'End date',
        isCurrent: 'I currently work here',
        description: 'Description',
        responsibilities: 'Responsibilities',
        responsibilitiesPlaceholder: 'Add a responsibility and press Enter',
        technologies: 'Technologies',
        technologiesPlaceholder: 'Search or add a technology',
      },
      deleteConfirm: {
        title: 'Delete this experience?',
        description: 'This will permanently remove this experience entry from your profile.',
      },
    },
    skills: {
      page: {
        title: 'Skills',
        subtitle: 'Rate your proficiency in the technologies you know.',
        add: 'Add skill',
        empty: 'No skills yet. Add your first one.',
        error: 'Failed to load your skills.',
      },
      form: {
        createTitle: 'Add skill',
        editTitle: 'Edit skill',
        subtitle: 'Pick a technology and rate your proficiency in it.',
      },
      fields: {
        technology: 'Technology',
        level: 'Proficiency (1-5)',
        yearsOfExperience: 'Years of experience',
        yearsOfExperienceShort: '{years} yrs',
        startedUsingYear: 'Started using (year)',
        isPrimary: 'Primary skill',
      },
      deleteConfirm: {
        title: 'Delete this skill?',
        description: 'This will permanently remove this skill from your profile.',
      },
    },
  },
}
