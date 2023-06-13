%% Rotina PRINCIPAL 
% Determina��o da localiza��o �tima de esta��es de monitoramento de
% qualidade de �gua
% DISSERTA��O DE MESTRADO 
% Aluno: Roberto Suse
% Orientador: Prof. Dr. Edevar Luvizotto Junior
% Ultima atualiza��o:  Novembro/2013
%%
% Limpeza de tela e de mem�ria
clc;                          %Limpa tela
clear all;                    %Limpa vari�veis
%% Dados de entrada
% Nome dos arquivos de dadps
Redefile  = 'exemplo3.inp';   %Nome do arquivo de dados .inp do Epanet
Coordfile = 'exemplo3.dat';   %Arquivo com coordenada dos nos extraido do inp
%%
% Crit�rio de cobertura e numero de esta��es a locar
criterio = 0.60;     %criterio de cobertura
num_est = 10;        %Numero de esta��es de montoramento (deve ser par)
%%
% Parametros do AG
NGen = 150;          %numero de gera��es
ind_pop = 20;       %Numero de individuos na popula��o
prob_mut = 0.05;    %Probabilidade de muta��o
%% Chamada ao EPANET Toolkit
epanetloadfile(Redefile); %Abre arquivo do Epanet
[Q] = getdata('EN_FLOW'); %Matriz da vaz�o Periodo Extensivo
Per = 1;                  %Periodo Desejado
%%
% Obtem informa��es da rede analizada
NoCont = getdata('EN_NODECOUNT');   %obtem numero de n�s da rede
LinkCont = getdata('EN_LINKCOUNT'); %Obtem numero mde elemnetos da rede
ND = NoCont;             %Indica a dimensao da matriz no. nos x no. de nos
MQ = zeros(ND,ND);       %Gera matriz de vaz�o nula
DM=getdata('EN_BASEDEMAND'); %Obtem vetor de demandas e armazena em DM
%%
% Informa��es dos n�s obtidas do arquivo de entrada INP do Epanet
for i=1:ND
Nix(i) = i;                  %Gera um vetor de indices dos n�s
[errorcode, N] = calllib('epanet2', 'ENgetnodeid',i,'');
Nid(i) = str2num(N);         %Gera um vetor de ididentifica��o id dos n�s
end
%%
% Informa��es relacionads aos tubos obtidas do arquivo INP
for i=1:LinkCont
[errorcode, N1,N2] = calllib('epanet2', 'ENgetlinknodes', i,0,0); 
VN1i(i)= N1; VN2i(i) = N2; %Vetores com indice dos n�s inicio e fim
[errorcode, Nu] = calllib('epanet2', 'ENgetlinkid',i,'');
VNu(i) = str2num(Nu);      %Vetor com Numero do elemento
[errorcode, Na] = calllib('epanet2','ENgetnodeid',N1, '');
VN1(i) = str2num(Na);      %Vetor com numero do n� inicio
[errorcode, Nb] = calllib('epanet2','ENgetnodeid',N2, '');
VN2(i) = str2num(Nb);      %Vetor com numero do n� jusante
[errorcode, N1i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN1(i)),0);
[errorcode, N2i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN2(i)),0);
N11(i) = str2num(N1i); N22(i) = str2num(N2i);
end
%%
% Le arquivo de coordenada dos n�s da rede do arquivo DAT
% contem a parte referente as coordenadas do arquivo Inp do Epanet
 [labels,x,y] = readColData(Coordfile,3,1);
% Obtem os valores extremos das coordenadas lidas
 [xmax,ind_xmax] = max(y(:,1));
 [xmin,ind_xmin] = min(y(:,1));
 [ymax,ind_ymax] = max(y(:,2));
 [ymin,ind_ymin] = min(y(:,2));
%%
% Define coordenadas da janela para o desenho da rede
 xmin = xmin-abs(xmax-xmin)*0.1;
 xmax = xmax+abs(xmax-xmin)*0.1;
 ymin = ymin-abs(ymax-ymin)*0.1;
 ymax = ymax+abs(ymax-ymin)*0.1;
%% 
% loop para desenho do tubos e aloca��o da matriz de vaz�es 
 subplot(1, 2, 1);
 axis([xmin xmax ymin ymax])
 axis off    
% Faz o Desenho da rede
hold on
for i=1:LinkCont
	Naa = find(Nid==N11(i));
	k = 1;
	while (N11(i) ~= x(k))
		k = k+1;
	end
	x1p = y(k,1); y1p =y(k,2);
	Nbb = find(Nid==N22(i));
	k = 1;
	while (N22(i) ~= x(k))
		k = k+1;
	end
	x2p = y(k,1); y2p =y(k,2); 
	line([x1p x2p], [y1p,y2p],'Color',[.0 .0 .0]); %Desenha as tubula��es
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
 subplot(1, 2, 1);
 axis([xmin xmax ymin ymax])
 axis off    
% Faz o Desenho da rede
hold on
% Redesenha nos e coloca o titulo principal
plot(y(:,1),y(:,2),'o','LineWidth',1,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','k',...
                'MarkerSize',4);
            delx = (xmax-xmin)*0.02;
            dely = (ymax-ymin)*0.04;
text(delx+y(:,1),dely+y(:,2),num2str(Nid(:)),...
     'HorizontalAlignment','left')
title('*** LOCA��O DE ESTA��ES DE MONITORAMENTO ***') 
%%
% Impress�o na tela dos dados de entrada
fprintf('\n================ Relator�o ============================\n');
fprintf('= Arquivo:                     %s \n', Redefile);
fprintf('= Numero total de n�s:         %d               \n',ND);
fprintf('= Numero total de elementos:   %d               \n', LinkCont);
fprintf('= Numero de esta��es a alocar: %d               \n',num_est);
fprintf('= Porcentagem de cobertura:    %d               \n',criterio*100);
fprintf('======================================================= \n');

%% INICIO DO PROCEDIMENTO 
% Vetor das demandas
prt = DM    % Vetor auxiliar utilizado para impress�o do vetor das demandas
% Obtem vetor de demandas nodais na forma propriada
DEM = DM'; %vetor demandas em coluna;
%%
% Obtem a matriz de fra��o de �gua
[f] = M_FRAC_AGUA (ND, MQ);              %Gera matriz da fra��o de �gua
clear prt;   %Limpa vetro auxiliar
prt = f      %Imprime matriz de fra��o de �gua
%%
% Obtem a Matriz de cobertura
[f] = MAT_COBERTURA (ND,f,criterio);     %Gera matriz de cobertura global
clear prt;   %Limpa vetro auxiliar
prt = f      %Imprime matriz de cobertura
%%
% Gerq Popula��o inicial
[POP] = POP_INICIAL(ind_pop, num_est,ND);%Gera popula��o inicial aleat�ria
%Limpa vetro auxiliar
for i=1:ind_pop
    clear prt
    prt = POP(i).cromossomo %Mostra individuos da popula��o inicial
end
%%
% Calcula a fun��o Objetivo para todos os individuos da popula��o inicial
[vajuste,POP] = F_OBJETIVO (ind_pop, f, POP, ND,num_est,DEM);  %Calcula fun��o objetivo da pop.
clear prt;         %Limpa vetro auxiliar
prt = vajuste      %Imprime valor da fun��o objetivo da popula��o inicial
%%
% Prepara para entrar no Laco do AG
 maxmax = 0;
 new_gera = 0;         %zera contador de gera��es
 disp('Gera��o Melhor Ajuste  Media Gera��o   Melhor Individuo')
%%
% Inicio do la�o das gera��es do AG
 while new_gera < NGen
 new_gera = new_gera+1;
 gerac(new_gera) = new_gera;                                    %Armazena vetor para plotagem
 [POP] = AG (num_est, ND, ind_pop, POP, prob_mut);              %gera nova popula��o
 [vajuste,POP] = F_OBJETIVO (ind_pop, f, POP, ND,num_est,DEM);  %Avalia popula��o
 % -------- Retem dados para impress�o e graficos ------------------------
 media(new_gera) = mean(vajuste);  %Media do vetor auxiliar das fun��es objetivos
 [maxi,ind_max] = max(vajuste);     %Localiza o maximo e o indice da melhor 
 maximo(new_gera) = maxi;           %Valor do melhor indiv�duo
 if maxmax < maxi
     maxmax = maxi;
     Melhor_de_todos = POP(ind_max).cromossomo;
 end
 Melhor_individuo = POP(ind_max).cromossomo; %Cromossomo da melhor solu��o
 fprintf('   %d  %15.4f %14.4f  ',new_gera, POP(ind_max).ajuste, media(new_gera));
 for i=1:num_est-1
 fprintf(' %d ',Nid(Melhor_individuo(i)));
 end
 fprintf(' %d \n',Nid(Melhor_individuo(num_est)));
 end
 % Fim do processamento das gera��es
%%
% Pega Indice  do melhor individuo para pintar no gr�fico
for i=1:num_est
     k = 1;
 while  (Nid(Melhor_de_todos(i)) ~= x(k))
     k = k+1;
 end
    xpl(i) = y(k,1); ypl(i) = y(k,2);
 end
 %% 
 % Desenha solu��o encontrada
 subplot(1, 2, 1);
 hold on
 plot(xpl,ypl,'o','LineWidth',1,...
                'MarkerEdgeColor','y',...
                'MarkerFaceColor','y',...
                'MarkerSize',12)
 %% 
 %Plota grafico dos ajustes do melhor indiciduo e da m�dia da popula��o
 subplot(1, 2, 2);
 plot(gerac,maximo,gerac,media);
 axis([1 NGen 0 maxmax*1.1])
 title('Evolu��o da converg�ncia');
 text(NGen*0.3,maxmax*0.76, 'Demanda Coberta =','FontSize',10);
  text(NGen*0.7,maxmax*0.76, int2str(maxmax),'FontSize',10);
 text(NGen*0.3,maxmax*0.70, 'Demanda Total =','FontSize',10);
  text(NGen*0.7,maxmax*0.70, int2str(sum(DM)),'FontSize',10);
 text(NGen*0.3,maxmax*0.64,'% Coberta =','FontSize',10);
  text(NGen*0.7,maxmax*0.64,strcat(int2str(round(maxmax/sum(DM)*100)),'  %'),'FontSize',10);
 lgd=legend('m�ximo','m�dia');
 set(lgd,'Location','SouthEast');
 xlabel('Numero de gera��es');
 ylabel('Fun��o objetivo');
%%
%Apresenta os n�s cobertos por cada uma das esta��es encontradas
 fprintf(' \n');
 fprintf(' \n ');
 fprintf('============================================ \n '); 
 fprintf('EST.  NOS COBERTOS \n');
 fprintf('============================================ \n '); 
for i=1:num_est
    fprintf('%4d', Nid(Melhor_de_todos(i)));
 for L = 1:1:ND
   if f(L, Nid(Melhor_de_todos(i))) == 1
    fprintf('%4d', L)
     end
 end
     fprintf(' \n ');
end
 fprintf('============================================ \n '); 
%%
 
 