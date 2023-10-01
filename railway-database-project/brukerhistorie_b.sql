/* Dere skal kunne registrere data om togruter. Dere skal legge inn data for de tre togrutene på
Nordlandsbanen som er beskrevet i vedlegget til denne oppgave. Dette kan gjøres med et skript,
dere trenger ikke å programmere støtte for denne funksjonaliteten. */


/* Tabell 1 */
insert into Vognoppsett(oppsettID)
values (1);

insert into Operatør(navn)
values ("SJ");

insert into Vogn(vognID, navn, type, operatør)
values (1, "SJ-sittevogn-1", "Sittevogn", "SJ");

insert into Vogn(vognID, navn, type, operatør)
values (2, "SJ-sittevogn-1", "Sittevogn", "SJ");

insert into SitteVogn(vognID, antallStolrader, stolerPrRad)
values (1, 3, 4);

insert into SitteVogn(vognID, antallStolrader, stolerPrRad)
values (2, 3, 4);

insert into VognIOppsett(oppsettID, vognID, nummer)
values (1, 1, 1);

insert into VognIOppsett(oppsettID, vognID, nummer)
values (1, 2, 2);

insert into Plass(plassnr, vognID)
values (1, 1);

insert into Plass(plassnr, vognID)
values (2, 1);

insert into Plass(plassnr, vognID)
values (3, 1);

insert into Plass(plassnr, vognID)
values (4, 1);

insert into Plass(plassnr, vognID)
values (5, 1);

insert into Plass(plassnr, vognID)
values (6, 1);

insert into Plass(plassnr, vognID)
values (7, 1);

insert into Plass(plassnr, vognID)
values (8, 1);

insert into Plass(plassnr, vognID)
values (9, 1);

insert into Plass(plassnr, vognID)
values (10, 1);

insert into Plass(plassnr, vognID)
values (11, 1);

insert into Plass(plassnr, vognID)
values (12, 1);

insert into Plass(plassnr, vognID)
values (1, 2);

insert into Plass(plassnr, vognID)
values (2, 2);

insert into Plass(plassnr, vognID)
values (3, 2);

insert into Plass(plassnr, vognID)
values (4, 2);

insert into Plass(plassnr, vognID)
values (5, 2);

insert into Plass(plassnr, vognID)
values (6, 2);

insert into Plass(plassnr, vognID)
values (7, 2);

insert into Plass(plassnr, vognID)
values (8, 2);

insert into Plass(plassnr, vognID)
values (9, 2);

insert into Plass(plassnr, vognID)
values (10, 2);

insert into Plass(plassnr, vognID)
values (11, 2);

insert into Plass(plassnr, vognID)
values (12, 2);


insert into Togrute(rutenr, operatør, startstasjon, endestasjon, oppsettID)
values (1, "SJ", "Trondheim S", "Bodø", 1);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "Trondheim S", NULL, '07:49:00', 1);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "Steinkjer", '09:51:00', '09:51:00', 2);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "Mosjøen", '13:20:00', '13:20:00', 3);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "I Rana", '14:31:00', '14:31:00', 4);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "Fauske", '16:49:00', '16:49:00', 5);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (1, "Bodø", '17:34:00', NULL, 6);

insert into Driftsdager(rutenr, ukedag)
values (1, "mandag");

insert into Driftsdager(rutenr, ukedag)
values (1, "tirsdag");

insert into Driftsdager(rutenr, ukedag)
values (1, "onsdag");

insert into Driftsdager(rutenr, ukedag)
values (1, "torsdag");

insert into Driftsdager(rutenr, ukedag)
values (1, "fredag");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (1, "Trondheim S", "Steinkjer", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (1, "Steinkjer", "Mosjøen", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (1, "Mosjøen", "Mo I Rana", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (1, "Mo I Rana", "Fauske", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (1, "Fauske", "Bodø", "true");

/* Tabell 2 */
insert into Vognoppsett(oppsettID)
values (2);

insert into Vogn(vognID, navn, type, operatør)
values (3, "SJ-sittevogn-1", "Sittevogn", "SJ");

insert into Vogn(vognID, navn, type, operatør)
values (4, "SJ-sovevogn-1", "Sovevogn", "SJ");

insert into SitteVogn(vognID, antallStolrader, stolerPrRad)
values (3, 3, 4);

insert into SoveVogn(vognID, antallSoveKupeer, sengerPrKupe)
values (4, 4, 2);

insert into VognIOppsett(oppsettID, vognID, nummer)
values (2, 3, 1);

insert into VognIOppsett(oppsettID, vognID, nummer)
values (2, 4, 2);

insert into Plass(plassnr, vognID)
values (1, 3);

insert into Plass(plassnr, vognID)
values (2, 3);

insert into Plass(plassnr, vognID)
values (3, 3);

insert into Plass(plassnr, vognID)
values (4, 3);

insert into Plass(plassnr, vognID)
values (5, 3);

insert into Plass(plassnr, vognID)
values (6, 3);

insert into Plass(plassnr, vognID)
values (7, 3);

insert into Plass(plassnr, vognID)
values (8, 3);

insert into Plass(plassnr, vognID)
values (9, 3);

insert into Plass(plassnr, vognID)
values (10, 3);

insert into Plass(plassnr, vognID)
values (11, 3);

insert into Plass(plassnr, vognID)
values (12, 3);

insert into Plass(plassnr, vognID)
values (1, 4);

insert into Plass(plassnr, vognID)
values (2, 4);

insert into Plass(plassnr, vognID)
values (3, 4);

insert into Plass(plassnr, vognID)
values (4, 4);

insert into Plass(plassnr, vognID)
values (5, 4);

insert into Plass(plassnr, vognID)
values (6, 4);

insert into Plass(plassnr, vognID)
values (7, 4);

insert into Plass(plassnr, vognID)
values (8, 4);

insert into Togrute(rutenr, operatør, startstasjon, endestasjon, oppsettID)
values (2, "SJ", "Trondheim S", "Bodø", 2);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Trondheim S", NULL, '23:05:00', 1);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Steinkjer", '00:57:00', '00:57:00', 2);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Mosjøen", '04:41:00', '04:41:00', 3);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Mo I Rana", '05:55:00', '05:55:00', 4);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Fauske", '08:19:00', '08:19:00', 5);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (2, "Bodø", '09:05:00', NULL, 6);

insert into Driftsdager(rutenr, ukedag)
values (2, "mandag");

insert into Driftsdager(rutenr, ukedag)
values (2, "tirsdag");

insert into Driftsdager(rutenr, ukedag)
values (2, "onsdag");

insert into Driftsdager(rutenr, ukedag)
values (2, "torsdag");

insert into Driftsdager(rutenr, ukedag)
values (2, "fredag");

insert into Driftsdager(rutenr, ukedag)
values (2, "lørdag");

insert into Driftsdager(rutenr, ukedag)
values (2, "søndag");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (2, "Trondheim S", "Steinkjer", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (2, "Steinkjer", "Mosjøen", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (2, "Mosjøen", "Mo I Rana", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (2, "Mo I Rana", "Fauske", "true");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (2, "Fauske", "Bodø", "true");

/* Tabell 3 */
insert into Vognoppsett(oppsettID)
values (3);

insert into Vogn(vognID, navn, type, operatør)
values (5, "SJ-sittevogn-1", "Sittevogn", "SJ");

insert into SitteVogn(vognID, antallStolrader, stolerPrRad)
values (5, 3, 4);

insert into VognIOppsett(oppsettID, vognID, nummer)
values (3, 5, 1);

insert into Plass(plassnr, vognID)
values (1, 5);

insert into Plass(plassnr, vognID)
values (2, 5);

insert into Plass(plassnr, vognID)
values (3, 5);

insert into Plass(plassnr, vognID)
values (4, 5);

insert into Plass(plassnr, vognID)
values (5, 5);

insert into Plass(plassnr, vognID)
values (6, 5);

insert into Plass(plassnr, vognID)
values (7, 5);

insert into Plass(plassnr, vognID)
values (8, 5);

insert into Plass(plassnr, vognID)
values (9, 5);

insert into Plass(plassnr, vognID)
values (10, 5);

insert into Plass(plassnr, vognID)
values (11, 5);

insert into Plass(plassnr, vognID)
values (12, 5);

insert into Togrute(rutenr, operatør, startstasjon, endestasjon, oppsettID)
values (3, "SJ", "Mo I Rana", "Trondheim S", 3);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (3, "Mo I Rana", NULL, '08:11:00', 1);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (3, "Mosjøen", '09:14:00', '09:14:00', 2);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (3, "Steinkjer", '12:31:00', '12:31:00', 3);

insert into Togrutetabell(rutenr, stasjon, ankomsttid, avgangstid, stasjonsnr)
values (3, "Trondheim S", '14:13:00', NULL, 4);

insert into Driftsdager(rutenr, ukedag)
values (3, "mandag");

insert into Driftsdager(rutenr, ukedag)
values (3, "tirsdag");

insert into Driftsdager(rutenr, ukedag)
values (3, "onsdag");

insert into Driftsdager(rutenr, ukedag)
values (3, "torsdag");

insert into Driftsdager(rutenr, ukedag)
values (3, "fredag");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (3, "Mosjøen", "Mo I Rana", "false");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (3, "Steinkjer", "Mosjøen", "false");

insert into DelstrekningPåRute(rutenr, startstasjon, endestasjon, kjørerHovedretning)
values (3, "Trondheim S", "Steinkjer", "false");