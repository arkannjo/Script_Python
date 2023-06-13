%% Matriz de Cobertura - Suse
%     16/03/2020
%% Limpeza 
close all; clear; rng(1); clear all; clc; 
%% Rede 
nome_da_rede='case1.inp';
%nome_da_rede='exemplo3.inp';
G=epanet(nome_da_rede); 

criterio = 0.20;
%% Aplicação 

G.openHydraulicAnalysis;
G.initializeHydraulicAnalysis;
G.runHydraulicAnalysis;
Q=G.getLinkFlows;
DEM=G.getNodeActualDemand;

Per = 1;   

G.closeHydraulicAnalysis;

Node_index=G.NodeIndex;
Num_nodes=G.NodeCount; 
LinkCont=G.LinkCount;
Num_reser=G.NodeReservoirCount;
Nid=Node_index;
N11_1=G.NodesConnectingLinksIndex;
N11=N11_1(:,1);
N22=N11_1(:,2);
N11=N11' ; N22=N22';

Node_coor=G.NodeCoordinates;
x=Nid;
y(:,1)=Node_coor{1,1};
y(:,2)=Node_coor{1,2};


for i=1:LinkCont
    Naa = find(Nid==N11(i)); % retorna a posição;
    Nbb = find(Nid==N22(i)); % retorna a posição;
    if Q(Per,i) > 0.0
        MQ(Nbb,Naa)= abs(Q(Per,i));
    else
        MQ(Naa,Nbb)= abs(Q(Per,i));
        %Matriz com as vazões
        
    end
end
if (Num_nodes-size(MQ,1)>0) % retorna o numero de linhas e de colunas
	MatrizZeros=zeros(Num_nodes-size(MQ,1),Num_nodes);
	MQ=vertcat(MQ,MatrizZeros); % concatena na vertical (linhas)
end

%% matriz de fração de água
ND=Num_nodes;
f=MQ;
for L = 1:1:ND;
    Vsoma(L) = 0;
    %Encntra a soma das vazoes para os nos de jusante
	for C=1:1:ND
		Vsoma(L) = Vsoma(L)+MQ(L,C);
	end
end
% ----------- fim totalizacao de vazoes aos nos -----------------------

% --------------- CRIA MATRIZ DE FRAÇÃO DE ÁGUA ------------------------
for L=1:1:ND
	for C=1:1:ND
		if Vsoma(L) == 0 
			Vsoma(L)=1;
		end 
		 f(L,C) = MQ(L,C)/Vsoma(L);
	end
end
% ---------- Da primeita parte (contribuição direta)  -------------------
f = f';  % Traspõe a matriz de fração para forma usual - vide texto
%---------------------------------------------------------------------
% Obtençao dos contribuiçoes de nós indiretamente contribuintes
% ----------------------------------------------------------------------
for i = 1:1:ND
    f(i,i) = 1; % fixa o valor 1 na diagonal da matriz de fração
end
% Inicio do calculo das contribições e armazenamento na matriz de fração
for C =2:1:ND
    for L=1:1:C-1
        if f(L,C) ~= 0
            ID = L;
            MUL = f(L,C);
            for K = 1:1:ID-1
                f(K,C) = f(K,C)+f(K,ID)*MUL;
            end
        end
    end
end

%% Matriz cobertura 0 ou 1

for L=1:1:ND 
    for C=1:1:ND
    if f(L,C) >= criterio
        f(L,C) = 1;
    else
        f(L,C) = 0;
    end
    end
end
FF = f;

%% Calculo da taxa de cobertura 

Sensores=importdata('x_CPF1_z5.mat'); % vetor que indica a presença de sensor 0 ou 1 
% Sensores=[9,5,14,8,18,17,19,11,3,10];
% Sensores=Sensores';

for j=1:size(Sensores,1)
    pop=find(Sensores(j,:)==1); % posicao em que há sensor
%     pop=Sensores;
    pop_todas{j}=pop;
    Aux=f(:,pop);
    Aux(:,(size(Aux,2))+1)=linspace(0,0,(size(Aux,1)));
    soma(j)=length(pop);
    soma_Aux=sum(Aux');
    Vetcob=soma_Aux;
    Aux22=find(Vetcob>0.5);
    Vetcob(Aux22)=1;
    VCD(j,:)= Vetcob.*DEM;
end

Sum_VCD=sum(VCD');
Sum_DEM=sum(DEM(1:end-Num_reser));

Cobertura=Sum_VCD*100/Sum_DEM
AvaliaCobertura=horzcat(soma',Cobertura');
AvaliaCobertura=sortrows(AvaliaCobertura,1);


