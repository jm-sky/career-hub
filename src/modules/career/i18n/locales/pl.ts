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
  },
}
