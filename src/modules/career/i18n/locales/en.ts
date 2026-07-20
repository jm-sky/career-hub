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
  },
}
