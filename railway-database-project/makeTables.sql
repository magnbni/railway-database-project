create table Operatør (
    navn varchar(30) not null,
    constraint operatør_pk primary key (navn)
);
create table Kunde (
    kundenr integer not null,
    navn varchar(30),
    epost varchar(60),
    telefonnr char(8),
    constraint kunde_pk primary key (kundenr)
);
create table Kundeordre (
    ordrenr integer not null,
    dato date,
    tid time,
    antall integer,
    kundenr integer not null,
    forekomstDato date not null,
    rutenr integer not null,
    constraint kundeordre_fk1 foreign key (forekomstDato, rutenr) references TogruteForekomst(dato, rutenr) on update cascade on delete cascade,
    constraint kundeordre_fk2 foreign key (kundenr) references Kunde(kundenr) on update cascade on delete cascade
);
create table Billett (
    billettnr integer not null,
    plassnr integer not null,
    vognID integer not null,
    ordrenr integer not null,
    startstasjon varchar(30) not null,
    endestasjon varchar(30) not null,
    constraint billett_pk primary key (billettnr),
    constraint billett_fk1 foreign key (plassnr, vognID) references Plass(plassnr, vognID) on update cascade on delete cascade,
    constraint billett_fk2 foreign key (ordrenr) references Kundeordre(ordrenr) on update cascade on delete cascade,
    constraint billett_fk3 foreign key (startstasjon) references JernbaneStasjon(navn) on update cascade on delete cascade,
    constraint billett_fk4 foreign key (endestasjon) references JernbaneStasjon(navn) on update cascade on delete cascade
);
create table Togrute (
    rutenr integer not null,
    operatør varchar(30) not null,
    startstasjon varchar(30) not null,
    endestasjon varchar(30) not null,
    oppsettID integer not null,
    constraint togrute_pk primary key (rutenr),
    constraint togrute_fk1 foreign key (operatør) references Operatør(navn) on update cascade on delete cascade,
    constraint togrute_fk2 foreign key (oppsettID) references Vognoppsett(oppsettID) on update cascade on delete cascade,
    constraint togrute_fk3 foreign key (startstasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint togrute_fk4 foreign key (endestasjon) references Jernbanestasjon(navn) on update cascade on delete cascade
);
create table Driftsdager (
    rutenr integer not null,
    ukedag varchar(7),
    constraint driftsdager_pk primary key (rutenr, ukedag),
    constraint driftsdager_fk foreign key (rutenr) references Togrute(rutenr) on update cascade on delete cascade
);
create table Togrutetabell (
    rutenr integer not null,
    stasjon varchar(30) not null,
    ankomsttid time,
    avgangstid time,
    stasjonsnr integer,
    constraint togrutetabell_pk primary key (rutenr, stasjon),
    constraint togrutetabell_fk1 foreign key (stasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint togrutetabell_fk2 foreign key (rutenr) references Togrute(rutenr) on update cascade on delete cascade
);
create table DelstrekningPåRute (
    rutenr integer not null,
    startstasjon varchar(30) not null,
    endestasjon varchar(30) not null,
    kjørerHovedretning varchar(5),
    constraint delstrekningPåRute_pk primary key (rutenr, startstasjon, endestasjon),
    constraint delstrekningPåRute_fk1 foreign key (rutenr) references Togrute(rutenr) on update cascade on delete cascade,
    constraint delstrekningPåRute_fk2 foreign key (startstasjon, endestasjon) references Delstrekning(startstasjon, endestasjon) on update cascade on delete cascade
);
create table Vogn (
    vognID integer not null,
    navn varchar(30) not null,
    type varchar(30) not null,
    operatør varchar(30) not null,
    constraint vogn_pk primary key (vognID),
    constraint vogn_fk foreign key (operatør) references Operatør(Navn) on update cascade on delete cascade
);
create table Vognoppsett (
    oppsettID integer not null,
    constraint vognoppsett_pk primary key (oppsettID)
);
create table VognIOppsett (
    oppsettID integer,
    vognID integer,
    nummer integer,
    constraint vognIOppsett_fk1 foreign key (oppsettID) references Vognoppsett(oppsettID) on update cascade on delete cascade,
    constraint vognIOppsett_fk2 foreign key (vognID) references Vogn(vognID) on update cascade on delete cascade
);
create table Sittevogn (
    vognID integer not null,
    antallStolrader integer not null,
    stolerPrRad integer not null,
    constraint sittevogn_pk primary key (vognID),
    constraint sittevogn_fk foreign key (vognID) references Vogn(vognID) on update cascade on delete cascade
);
create table Sovevogn (
    vognID integer not null,
    antallSovekupeer integer not null,
    sengerPrKupe integer not null,
    constraint sovevogn_pk primary key (vognID),
    constraint sovevogn_fk foreign key (vognID) references Vogn(vognID) on update cascade on delete cascade
);
create table Plass (
    plassnr integer not null,
    vognID integer not null,
    constraint plass_pk primary key (plassnr, vognID),
    constraint plass_fk foreign key (vognID) references Vogn(vognID) on update cascade on delete cascade
);
create table Togruteforekomst (
    dato date not null,
    rutenr integer not null,
    constraint togruteforekomst_pk primary key (dato, rutenr),
    constraint togruteforekomst_fk foreign key (rutenr) references Togrute(rutenr) on update cascade on delete cascade
);
create table Banestrekning (
    navn varchar(30) not null,
    fremdriftsenergitype varchar(10),
    startstasjon varchar(30) not null,
    endestasjon varchar(30) not null,
    constraint banestrekning_pk primary key (navn),
    constraint banestrekning_fk1 foreign key (startstasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint banestrekning_fk2 foreign key (endestasjon) references Jernbanestasjon(navn) on update cascade on delete cascade
);
create table Delstrekning (
    startstasjon varchar(30) not null,
    endestasjon varchar(30) not null,
    lengde integer,
    erEnkeltspor varchar(5),
    banestrekning varchar(30) not null,
    constraint delstrekning_pk primary key (startstasjon, endestasjon),
    constraint delstrekning_fk1 foreign key (startstasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint delstrekning_fk2 foreign key (endestasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint delstrekning_fk3 foreign key (banestrekning) references Banestrekning(navn) on update cascade on delete cascade
);
create table StasjonPåBanestrekning (
    stasjon varchar(30) not null,
    banestrekning varchar(30) not null,
    constraint stasjonPåBanestrekning_pk primary key (stasjon, banestrekning),
    constraint stasjonPåBanestrekning_fk1 foreign key (stasjon) references Jernbanestasjon(navn) on update cascade on delete cascade,
    constraint stasjonPåBanestrekning_fk2 foreign key (banestrekning) references Banestrekning(navn) on update cascade on delete cascade
);
create table Jernbanestasjon (
    navn varchar (30) not null,
    moh integer not null,
    constraint jernbanestasjon_pk primary key (navn)
);