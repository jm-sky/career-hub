# CareerHub — Funkcjonalności

Pełna lista funkcjonalności w języku polskim (zobacz [README.md](./README.md) po angielsku).

## Profil zawodowy

- Kreator profilu w wielu krokach z automatycznym zapisem szkicu po każdym kroku
- Wskaźnik kompletności profilu
- Trzy poziomy widoczności: Prywatny, Znajomi, Publiczny
- Publiczna strona profilu pod unikalnym adresem (slug), przyjazna SEO
- Dane kontaktowe, nagłówek, podsumowanie, zdjęcie profilowe

## Doświadczenie i projekty

- Bogate dane dla każdej roli: firma, stanowisko, typ zatrudnienia, daty, obowiązki, technologie
- Projekty dokumentowane niezależnie od ról zawodowych, następnie jawnie łączone z jedną lub kilkoma rolami i umiejętnościami — wspiera portfolio łączące pracę z różnych firm
- Anonimizacja — ukrycie prawdziwej nazwy firmy/klienta za placeholderem dla projektów objętych NDA
- Sekcje uporządkowane przez użytkownika (przeciągnij-i-upuść)

## Umiejętności

- Kategoryzowane umiejętności (Techniczne/Narzędzia/Miękkie) z poziomem 1-5 i latami doświadczenia
- Możliwość powiązania umiejętności z konkretnymi projektami
- Sugestie umiejętności generowane przez AI dla wybranej roli (Pro/Expert)

## Generowanie CV

- Wiele nazwanych wersji CV na profil — każda jako wyselekcjonowany wybór doświadczeń, projektów, umiejętności, wykształcenia i certyfikatów z głównego profilu
- Opcjonalne własne podsumowanie nadpisujące domyślne, wybór szablonu
- Asynchroniczne generowanie PDF w tle; PDF-y w planie Free ze znakiem wodnym

## Import/Eksport

- Import z LinkedIn (zadanie asynchroniczne)
- Awaryjny parser tekstu wklejonego ręcznie
- Pełny eksport JSON danych profilu

## Funkcje AI (Pro/Expert)

- Optymalizacja opisu obowiązków/stanowiska
- Sugerowanie brakujących obowiązków dla roli i poziomu seniority
- Analiza luk względem docelowej roli (dopasowanie, mocne strony, luki, rekomendacje)

## Konto i bezpieczeństwo

- Rejestracja i logowanie (email/hasło), logowanie przez Google/Facebook/GitHub
- Weryfikacja email, uwierzytelnianie dwuskładnikowe (TOTP, WebAuthn/passkeys)
- Reset i zmiana hasła, ochrona reCAPTCHA v3
- Zarządzanie sesją (JWT z odświeżaniem), usuwanie konta zgodne z RODO

## Plany subskrypcji

| Plan | Cena | Funkcje |
|------|------|---------|
| **Free** | 0 zł/mies. | Bogaty profil, podstawowy profil publiczny, 2 wersje CV, eksport PDF ze znakiem wodnym, import z LinkedIn |
| **Pro** | 19 zł/mies. | Wszystko z Free + nielimitowane wersje CV, brak znaku wodnego, generator one-pagera, podstawowe sugestie AI, zaawansowana kontrola prywatności |
| **Expert** | 50 zł/mies. | Wszystko z Pro + pogłębiona analiza AI, własna domena, dostęp do API, priorytetowe wsparcie, kopie zapasowe i wersjonowanie |

## Wielojęzyczność i motywy

- Pełne wsparcie języka angielskiego i polskiego
- Automatyczne wykrywanie języka przeglądarki, ręczne przełączanie
- Tryb ciemny z wykrywaniem preferencji systemowych
