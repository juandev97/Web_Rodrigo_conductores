create database Web_rodrigo;
GO 
use Web_rodrigo;
GO

create table Datos_conductor(
	ID int identity primary key,
	Nombre varchar(250) not null,
	CC varchar(250) not null,
	Direccion varchar(250) not null,
	Email varchar(250) not null,
	propietario bit not null,
	tipo_vehiculo varchar(15) not null,
	fecha_cumple date not null,
	path_firma varchar(350)
	)

create table Registro(
	ID int identity primary key,
	FK_conductor int not null,
	fecha date not null,
	tipo varchar(50) not null,
	foreign key (FK_conductor) references Datos_conductor(ID) on delete cascade
	)


	/*alter table Registro 
	drop constraint FK_conductor
	
	alter table Registro 
	Add constraint FK_conductor
	foreign key (FK_conductor) references Datos_conductor(ID) on delete cascade

	*/


--------------------------------Triggers


------update
create trigger Registrar_actualizacion 
on Datos_conductor
after update
as
Declare @ID_c int

select @ID_c = ID from inserted

insert into Registro values(@ID_c, getdate(),'U')
go

-----------insert 
create trigger Registrar_insercion 
on Datos_conductor
after insert
as
Declare @ID_c int

select @ID_c = ID from inserted

insert into Registro values(@ID_c, getdate(),'I')
go





insert into Datos_conductor values(
'Jesus', '101211', 'av paz','j@h.com',
1,'T',getdate(), 'asd')

update Datos_conductor set Nombre= 'pedro' where ID=1