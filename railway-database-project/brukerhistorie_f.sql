/* Det skal legges inn nødvendige data slik at systemet kan håndtere billettkjøp for de tre togrutene
på Nordlandsbanen, mandag 3. april og tirsdag 4. april i år. Dette kan gjøres med et skript, dere
trenger ikke å programmere støtte for denne funksjonaliteten */

/* Opprette togruteforekomster */
insert into Togruteforekomst(dato, rutenr)
values ("2023-03-04", "1");

insert into Togruteforekomst(dato, rutenr)
values ("2023-03-04", "2");

insert into Togruteforekomst(dato, rutenr)
values ("2023-03-04", "3");

insert into Togruteforekomst(dato, rutenr)
values ("2023-04-04", "1");

insert into Togruteforekomst(dato, rutenr)
values ("2023-04-04", "2");

insert into Togruteforekomst(dato, rutenr)
values ("2023-04-04", "3");