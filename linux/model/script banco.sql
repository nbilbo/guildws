
create table cargo(idcargo integer primary key autoincrement,cargo varchar(15) not null,constraint unique_cargo unique (cargo));

create table jogador(idjogador integer primary key autoincrement,nome char(15) not null,id_cargo integer not null,foreign key(id_cargo) references cargo(idcargo), constraint unique_nome unique (nome));

create table data(iddata integer primary key autoincrement,data date);

create table gp(id_data integer not null, nome char(15), cargo char(15), gp integer not null,foreign key(id_data) references data(iddata));

insert into cargo(idcargo, cargo)values(null, "novato");

insert into cargo(idcargo, cargo)values(null, "explorador");

insert into cargo(idcargo, cargo)values(null, "herdeiro");

insert into cargo(idcargo, cargo)values(null, "lider");

create view v_jogador as select jogador.idjogador, jogador.nome, cargo.cargo from jogador inner join cargo on cargo.idcargo = jogador.id_cargo order by jogador.id_cargo desc, jogador.nome;
create view v_gp as select data.iddata, data.data, gp.nome, gp.cargo, gp.gp from data inner join gp on data.iddata = gp.id_data order by gp.gp desc;
