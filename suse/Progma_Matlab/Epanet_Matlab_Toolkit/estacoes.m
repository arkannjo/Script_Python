function varargout = estacoes(varargin)
% ESTACOES M-file for estacoes.fig
%      ESTACOES, by itself, creates a new ESTACOES or raises the existing
%      singleton*.
%
%      H = ESTACOES returns the handle to a new ESTACOES or the handle to
%      the existing singleton*.
%
%      ESTACOES('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ESTACOES.M with the given input arguments.
%
%      ESTACOES('Property','Value',...) creates a new ESTACOES or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before estacoes_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to estacoes_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help estacoes

% Last Modified by GUIDE v2.5 25-Jun-2013 15:44:54

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @estacoes_OpeningFcn, ...
                   'gui_OutputFcn',  @estacoes_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before estacoes is made visible.
function estacoes_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to estacoes (see VARARGIN)

% Choose default command line output for estacoes
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes estacoes wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = estacoes_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
clear all; %Limpa variáveis
obj = findobj(gcf,'Tag','ed_Rede');
wdsfile = get(obj,'String');  %Arquivo simulado
epanetloadfile(wdsfile);
[Q] = getdata('EN_FLOW');    %Matriz da vazão Periodo Extensivo
Per = 1;                     %Periodo Desejado
%printouts
clc;
NoCont = getdata('EN_NODECOUNT');   %obtem numero de nós da rede
LinkCont = getdata('EN_LINKCOUNT'); %Obtem numero mde elemnetos da rede
ND = NoCont;             %Indica a dimensao da matriz no. nos x no. de nos
MQ = zeros(ND,ND);
DM= getdata('EN_BASEDEMAND');
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
axes1.visible = true;
%Le arquivo de coordenada dos nós da rede
 obj = findobj(gcf,'Tag','ed_Coord');
 coordfile = get(obj,'String');  %Arquivo simulado
 [labels,x,y] = readColData(coordfile,3,1);
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
                'MarkerSize',6)
 axis([xmin xmax ymin ymax])
 axis off
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
  line([x1p x2p], [y1p,y2p],'Color',[.0 .0 .0]);
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
text(1.01*y(:,1),1.04*y(:,2),num2str(Nid(:)),...
     'HorizontalAlignment','left')
title('*** LOCAÇÃO DE ESTAÇÕES DE MONITORAMENTO ***') 
obj = findobj(gcf,'Tag','ed_Cob');
criterio = str2double(get(obj,'String'));  %criterio de cobertura
%criterio = 0.8;    

%---------------- PARAMETROS DO AG ----------------------------------
obj = findobj(gcf,'Tag','ed_Ger');
NF = str2double(get(obj,'String')); 
NGen = fix(NF);      %Numero de gerações
obj = findobj(gcf,'Tag','ed_Pop');
NF = str2double(get(obj,'String')); 
ind_pop = fix(NF);   %Numero de individuos na população      
obj = findobj(gcf,'Tag','ed_Est');
NF = str2double(get(obj,'String')); 
num_est = fix(NF);  %Numero de estações de montoramento 
obj = findobj(gcf,'Tag','ed_Mut');
prob_mut = str2double(get(obj,'String')); %Probabilidade de mutação
%prob_mut = 0.07;    
%--------------- FIM DA ENTRADA DE DADOS ----------------------------
fprintf('\n================ Relatorío ============================\n');
fprintf('= Arquivo:                     %s \n', wdsfile);
fprintf('= Numero total de nós:         %d               \n',ND);
fprintf('= Numero total de elementos:   %d               \n', LinkCont);
fprintf('= Numero de estações a alocar: %d               \n',num_est);
fprintf('= Porcentagem de cobertura:    %d               \n',criterio*100);
fprintf('======================================================= \n');
h = findobj(gcf,'Tag','text10');
set(h,'String',ND);
% ================ INICIO DO PROCEDIMENTO ============================
DEM = DM'; %vetor demandas em coluna;
[f] = M_FRAC_AGUA (ND, MQ);              %Gera matriz da fração de água
[f] = MAT_COBERTURA (ND,f,criterio);     %Gera matriz de cobertura global
[POP] = POP_INICIAL(ind_pop, num_est,ND);%Gera população inicial aleatória
[vajuste,POP] = F_OBJETIVO (ind_pop, f, POP, ND,num_est,DEM);  %Calcula função objetivo da pop.

%-------------- Chama a rotina de AG ------------------------------------
 new_gera = 0;         %zera contador de gerações
 disp('Geração Melhor Ajuste  Media Geração   Melhor Individuo')
 while new_gera < NGen
 new_gera = new_gera+1;
 [POP] = AG (num_est, ND, ind_pop, POP, prob_mut);              %gera nova população
 [vajuste,POP] = F_OBJETIVO (ind_pop, f, POP, ND,num_est,DEM);  %Avalia população

 % -------- Retem dados para impressão e graficos ------------------------
 meida = mean(vajuste);  %Media do vetor auxiliar das funções objetivos
 [maximo,ind_max] = max(vajuste); %Localiza o maximo e o indice da melhor 
 Melhor_individuo = POP(ind_max).cromossomo; %Cromossomo da melhor solução
 fprintf('   %d  %15.4f %14.4f  ',new_gera, POP(ind_max).ajuste, meida);
 for i=1:num_est-1
 fprintf(' %d ',Nid(Melhor_individuo(i)));
 end
 fprintf(' %d \n',Nid(Melhor_individuo(num_est)));

 % ----------------------------------------------------------------------
 end         %Fim do processamento das gerações
 
 for i=1:num_est
     k = 1;
 while  (Nid(Melhor_individuo(i)) ~= x(k))
     k = k+1;
 end
    xpl(i) = y(k,1); ypl(i) = y(k,2);
 end
 hold on
 plot(xpl,ypl,'o','LineWidth',1,...
                'MarkerEdgeColor','y',...
                'MarkerFaceColor','y',...
                'MarkerSize',6)

function ed_Rede_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Rede (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Rede as text
%        str2double(get(hObject,'String')) returns contents of ed_Rede as a double


% --- Executes during object creation, after setting all properties.
function ed_Rede_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Rede (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Coord_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Coord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Coord as text
%        str2double(get(hObject,'String')) returns contents of ed_Coord as a double


% --- Executes during object creation, after setting all properties.
function ed_Coord_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Coord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Pop_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Pop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Pop as text
%        str2double(get(hObject,'String')) returns contents of ed_Pop as a double


% --- Executes during object creation, after setting all properties.
function ed_Pop_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Pop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Mut_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Mut (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Mut as text
%        str2double(get(hObject,'String')) returns contents of ed_Mut as a double


% --- Executes during object creation, after setting all properties.
function ed_Mut_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Mut (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Ger_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Ger (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Ger as text
%        str2double(get(hObject,'String')) returns contents of ed_Ger as a double


% --- Executes during object creation, after setting all properties.
function ed_Ger_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Ger (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Cob_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Cob (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Cob as text
%        str2double(get(hObject,'String')) returns contents of ed_Cob as a double


% --- Executes during object creation, after setting all properties.
function ed_Cob_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Cob (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ed_Est_Callback(hObject, eventdata, handles)
% hObject    handle to ed_Est (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ed_Est as text
%        str2double(get(hObject,'String')) returns contents of ed_Est as a double


% --- Executes during object creation, after setting all properties.
function ed_Est_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ed_Est (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


