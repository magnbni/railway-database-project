/* Databasen skal kunne registrere data om alle jernbanestrekninger i Norge. Dere skal legge inn
data for Nordlandsbanen (som vist i figuren). Dette kan gjøres med et skript, dere trenger ikke å
programmere støtte for denne funksjonaliteten. */

insert into Jernbanestasjon(navn, moh)
values ("Trondheim S", 5);

insert into Jernbanestasjon(navn, moh)
values ("Steinkjer", 4);

insert into Jernbanestasjon(navn, moh)
values ("Mosjøen", 7);

insert into Jernbanestasjon(navn, moh)
values ("Mo I Rana", 4);

insert into Jernbanestasjon(navn, moh)
values ("Fauske", 34);

insert into Jernbanestasjon(navn, moh)
values ("Bodø", 4);

insert into Banestrekning(navn, fremdriftsenergitype, startstasjon, endestasjon)
values ("Nordlandsbanen", "diesel", "Trondheim", "Bodø");

insert into Delstrekning(startstasjon, endestasjon, lengde, erEnkeltspor, banestrekning)
values ("Trondheim", "Steinkjer", 120, "false", "Nordlandsbanen");

insert into Delstrekning(startstasjon, endestasjon, lengde, erEnkeltspor, banestrekning)
values ("Steinkjer", "Mosjøen", 280, "true", "Nordlandsbanen");

insert into Delstrekning(startstasjon, endestasjon, lengde, erEnkeltspor, banestrekning)
values ("Mosjøen", "Mo I Rana", 90, "true", "Nordlandsbanen");

insert into Delstrekning(startstasjon, endestasjon, lengde, erEnkeltspor, banestrekning)
values ("Mo I Rana", "Fauske", 170, "true", "Nordlandsbanen");

insert into Delstrekning(startstasjon, endestasjon, lengde, erEnkeltspor, banestrekning)
values ("Fauske", "Bodø", 60, "true", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("Trondheim S", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("Steinkjer", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("Mosjøen", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("I Rana", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("Fauske", "Nordlandsbanen");

insert into StasjonPåBanestrekning(stasjon, banestrekning)
values ("Bodø", "Nordlandsbanen");