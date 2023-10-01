/* Kjør denne filen for å klarere databasen */


delete from Kundeordre where ordrenr > 0;

delete from Billett where billettnr > 0;

delete from Jernbanestasjon where moh > 0;

delete from StasjonPåBanestrekning where banestrekning = "Nordlandsbanen";

delete from Delstrekning where lengde > 0;

delete from Banestrekning where navn = "Nordlandsbanen";

delete from Togruteforekomst where rutenr > 0;

delete from Plass where plassnr > 0;

delete from Sovevogn where vognID > 0;

delete from Sittevogn where vognID > 0;

delete from VognIOppsett where vognID > 0;

delete from Vogn where vognID > 0;

delete from Vognoppsett where oppsettID > 0;

delete from DelstrekningPåRute where rutenr > 0;

delete from Togrutetabell where rutenr > 0;

delete from Driftsdager where rutenr > 0;

delete from Togrute where rutenr > 0;

delete from Kunde where kundenr > 0;

delete from Operatør where navn = "SJ";