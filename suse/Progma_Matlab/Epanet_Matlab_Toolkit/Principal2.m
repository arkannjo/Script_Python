%% Rotina PRINCIPAL 
% Determinação da localização ótima de estações de monitoramento de
% qualidade de água
% DISSERTAÇÂO DE MESTRADO 
% Aluno: Roberto Suse
% Orientador: Prof. Dr. Edevar Luvizotto Junior
% Ultima atualização:  Novembro/2013
%%
% Limpeza de tela e de memória
clc;                          %Limpa tela
clear all;                    %Limpa variáveis
%% Dados de entrada
% Nome dos arquivos de dadps
Redefile  = 'exemplo3.inp';   %Nome do arquivo de dados .inp do Epanet
Coordfile = 'exemplo3.dat';   %Arquivo com coordenada dos nos extraido do inp
%%
% Critério de cobertura e numero de estações a locar
criterio = 0.60;     %criterio de cobertura
num_est = 10;        %Numero de estações de montoramento (deve ser par)
%%


epanetloadfile(Redefile); %Abre arquivo do Epanet
[Q] = getdata('EN_FLOW'); %Matriz da vazão Periodo Extensivo
Per = 1;                  %Periodo Desejado
%%
% Obtem informações da rede analizada
NoCont = getdata('EN_NODECOUNT');   %obtem numero de nós da rede
LinkCont = getdata('EN_LINKCOUNT'); %Obtem numero mde elemnetos da rede
ND = NoCont;             %Indica a dimensao da matriz no. nos x no. de nos
MQ = zeros(ND,ND);       %Gera matriz de vazão nula
DM=getdata('EN_BASEDEMAND'); %Obtem vetor de demandas e armazena em DM
%%


% Informações dos nós obtidas do arquivo de entrada INP do Epanet
for i=1:ND
	Nix(i) = i;                  %Gera um vetor de indices dos nós
	[errorcode, N] = calllib('epanet2', 'ENgetnodeid',i,'');
	Nid(i) = str2num(N);         %Gera um vetor de ididentificação id dos nós
end
%%


% Informações relacionads aos tubos obtidas do arquivo INP
for i=1:LinkCont
	[errorcode, N1,N2] = calllib('epanet2', 'ENgetlinknodes', i,0,0); 
	VN1i(i)= N1; VN2i(i) = N2; %Vetores com indice dos nós inicio e fim
	[errorcode, Nu] = calllib('epanet2', 'ENgetlinkid',i,'');
	VNu(i) = str2num(Nu);      %Vetor com Numero do elemento
	[errorcode, Na] = calllib('epanet2','ENgetnodeid',N1, '');
	VN1(i) = str2num(Na);      %Vetor com numero do nó inicio
	[errorcode, Nb] = calllib('epanet2','ENgetnodeid',N2, '');
	VN2(i) = str2num(Nb);      %Vetor com numero do nó jusante
	[errorcode, N1i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN1(i)),0);
	[errorcode, N2i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN2(i)),0);
	N11(i) = str2num(N1i); N22(i) = str2num(N2i);
end
%%


% Faz o Desenho da rede
hold on
for i=1:LinkCont
	Naa = find(Nid==N11(i));
	Nbb = find(Nid==N22(i));
	
	if Q(Per,i) > 0.0
		MQ(Nbb,Naa)= abs(Q(Per,i));
	else
		MQ(Naa,Nbb)= abs(Q(Per,i));
	end
end;
%%
% fecha o Epanet tool kit
epanetclose();
%%

%% INICIO DO PROCEDIMENTO 
% Vetor das demandas
prt = DM    % Vetor auxiliar utilizado para impressão do vetor das demandas
% Obtem vetor de demandas nodais na forma propriada
DEM = DM'; %vetor demandas em coluna;
%%
% Obtem a matriz de fração de água
[f] = M_FRAC_AGUA (ND, MQ);              %Gera matriz da fração de água
clear prt;   %Limpa vetro auxiliar
prt = f      %Imprime matriz de fração de água
%%
% Obtem a Matriz de cobertura
[f] = MAT_COBERTURA (ND,f,criterio);     %Gera matriz de cobertura global
clear prt;   %Limpa vetro auxiliar
prt = f      %Imprime matriz de cobertura