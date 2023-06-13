 clc
clear all;                   %Limpa variáveis
wdsfile='Net1.inp';          %Arquivo simulado
epanetloadfile(wdsfile);
[Q] = getdata('EN_FLOW');    %Matriz da vazão Periodo Extensivo
Per = 1;                     %Periodo Desejado
%printouts
clc;
NoCont = getdata('EN_NODECOUNT');   %obtem numero de nós da rede
LinkCont = getdata('EN_LINKCOUNT'); %Obtem numero mde elemnetos da rede
ND = NoCont;             %Indica a dimensao da matriz no. nos x no. de nos
MQ = zeros(ND,ND);
DM=getdata('EN_BASEDEMAND');
for i=1:ND
Nix(i) = i;           %gera um vetor de indices
[errorcode, N] = calllib('epanet2', 'ENgetnodeid',i,'');
Nid(i) = str2num(N);  %gera um vetro de id
end
for i=1:LinkCont
[errorcode, N1,N2] = calllib('epanet2', 'ENgetlinknodes', i,0,0); 
VN1i(i)= N1; VN2i(i) = N2; %Vetor com indice dos nós inicio e fim
[errorcode, Nu] = calllib('epanet2', 'ENgetlinkid',i,'');
VNu(i) = str2num(Nu);      %Vetor com Numero do elemento
[errorcode, Na] = calllib('epanet2','ENgetnodeid',N1, '');
VN1(i) = str2num(Na);      %Vetor com numero do nó inicio
[errorcode, Nb] = calllib('epanet2','ENgetnodeid',N2, '');
VN2(i) = str2num(Nb);      %Vetor com numero do nó jusante
%fprintf('Nu %s  NI = %s  NF = %s  Q = %6.2f \n',Nu,Na, Nb,Q(Per,i));
[errorcode, N1i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN1(i)),0);
[errorcode, N2i] = calllib('epanet2', 'ENgetnodeindex',num2str(VN2(i)),0);
N11(i) = str2num(N1i); N22(i) = str2num(N2i);
%fprintf('%d %d  %d \n',i, N1i,N2i);
end
%Le arquivo de coordenada dos nós da rede
 [labels,x,y] = readColData('Nod_Coord.dat',3,1);
 [xmax,ind_xmax] = max(y(:,1));
 [xmin,ind_xmin] = min(y(:,1));
 [ymax,ind_ymax] = max(y(:,2));
 [ymin,ind_ymin] = min(y(:,2));
 xmin = xmin-abs(xmax-xmin)*0.1;
 xmax = xmax+abs(xmax-xmin)*0.1;
 ymin = ymin-abs(ymax-ymin)*0.1;
 ymax = ymax+abs(ymax-ymin)*0.1;
 plot(y(:,1),y(:,2),'o','LineWidth',1,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','k',...
                'MarkerSize',5)
 axis([xmin xmax ymin ymax])
 axis off
for i=1:LinkCont
Naa = find(Nid==N11(i));
  k = 1;
  while (N11(i) ~= x(k))
      k = k+1;
  end
  x1p(i) = y(k,1); y1p(i) =y(k,2);
 Nbb = find(Nid==N22(i));
  k = 1;
  while (N22(i) ~= x(k))
      k = k+1;
  end
  x2p(i) = y(k,1); y2p(i) =y(k,2); 
  line([x1p(i) x2p(i)], [y1p(i),y2p(i)],'Color',[.0 .0 .0]);
if Q(Per,i) > 0.0
    MQ(Nbb,Naa)= abs(Q(Per,i));
else
    MQ(Naa,Nbb)= abs(Q(Per,i));
end
end;
epanetclose();
hold on
 plot(y(:,1),y(:,2),'o','LineWidth',1,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','k',...
                'MarkerSize',6)
