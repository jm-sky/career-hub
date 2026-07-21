export const careerPl = {
  career: {
    profile: {
      page: {
        title: 'Mój profil',
        subtitle: 'To na podstawie tych danych powstają Twoje CV.',
        save: 'Zapisz',
        error_prefix: 'Nie udało się wczytać profilu.',
        completeness: 'Kompletność profilu: {score}%',
      },
      fields: {
        headline: {
          label: 'Nagłówek',
          placeholder: 'np. Starszy Inżynier Backend',
        },
        summary: {
          label: 'Podsumowanie',
          placeholder: 'Krótki opis Twojego doświadczenia zawodowego.',
        },
        location: {
          label: 'Lokalizacja',
          placeholder: 'np. Warszawa, Polska',
        },
        visibility: {
          label: 'Widoczność',
          options: {
            PRIVATE: 'Prywatny — widoczny tylko dla Ciebie',
            FRIENDS: 'Znajomi — wkrótce, obecnie działa jak Prywatny',
            PUBLIC: 'Publiczny — widoczny dla każdego z linkiem',
          },
        },
        contact: {
          title: 'Dane kontaktowe',
          subtitle: 'Widoczne tylko dla Ciebie — nie pojawiają się na publicznym profilu.',
          email: 'Email',
          phone: 'Telefon',
          linkedin: 'LinkedIn',
          website: 'Strona WWW',
        },
        slug: {
          label: 'Adres publicznego profilu',
        },
      },
    },
    publicProfile: {
      page: {
        title: 'Profil',
      },
      not_found: 'Ten profil nie istnieje lub nie jest publiczny.',
      error: 'Nie udało się wczytać tego profilu.',
    },
    experiences: {
      page: {
        title: 'Doświadczenie',
        subtitle: 'Twoja historia zawodowa — na jej podstawie powstają CV.',
        add: 'Dodaj doświadczenie',
        empty: 'Brak wpisów doświadczenia. Dodaj pierwszy.',
        error: 'Nie udało się wczytać Twojego doświadczenia.',
      },
      form: {
        createTitle: 'Dodaj doświadczenie',
        editTitle: 'Edytuj doświadczenie',
        subtitle: 'Opisz stanowisko, jego daty oraz użyte technologie.',
      },
      fields: {
        companyName: 'Firma',
        position: 'Stanowisko',
        employmentType: 'Rodzaj zatrudnienia',
        employmentTypePlaceholder: 'np. full_time, kontrakt, freelance',
        startDate: 'Data rozpoczęcia',
        endDate: 'Data zakończenia',
        isCurrent: 'Obecnie tu pracuję',
        description: 'Opis',
        responsibilities: 'Obowiązki',
        responsibilitiesPlaceholder: 'Dodaj obowiązek i naciśnij Enter',
        technologies: 'Technologie',
        technologiesPlaceholder: 'Wyszukaj lub dodaj technologię',
      },
      deleteConfirm: {
        title: 'Usunąć to doświadczenie?',
        description: 'Ten wpis doświadczenia zostanie trwale usunięty z Twojego profilu.',
      },
    },
    skills: {
      page: {
        title: 'Umiejętności',
        subtitle: 'Oceń swój poziom biegłości w znanych technologiach.',
        add: 'Dodaj umiejętność',
        empty: 'Brak umiejętności. Dodaj pierwszą.',
        error: 'Nie udało się wczytać Twoich umiejętności.',
      },
      form: {
        createTitle: 'Dodaj umiejętność',
        editTitle: 'Edytuj umiejętność',
        subtitle: 'Wybierz technologię i oceń swój poziom biegłości.',
      },
      fields: {
        technology: 'Technologia',
        level: 'Poziom biegłości (1-5)',
        yearsOfExperience: 'Lata doświadczenia',
        yearsOfExperienceShort: '{years} lat',
        startedUsingYear: 'Rok rozpoczęcia',
        isPrimary: 'Umiejętność kluczowa',
      },
      deleteConfirm: {
        title: 'Usunąć tę umiejętność?',
        description: 'Ta umiejętność zostanie trwale usunięta z Twojego profilu.',
      },
    },
  },
}
