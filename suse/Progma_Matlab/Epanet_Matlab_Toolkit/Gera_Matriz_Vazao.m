%Matriz de Vazão de CDovertura
%Usando o Epanet toolkit

wdsfile='Net1.inp';
pumps={'9'};
tanks={'2'};
epanetloadfile(wdsfile);



%printouts
fprintf('nodes = %d\n',getdata('EN_NODECOUNT'))
fprintf('links = %d\n',getdata('EN_LINKCOUNT'))
fprintf('tanks = %d\n',lentanks)
fprintf('pumps = %d\n',lenpumps)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% S O L V E   H Y D R A U L I C S
[d_N,tv] = getdata('EN_DEMAND');
[P] = getdata('EN_PRESSURE');
[Q] = getdata('EN_FLOW');
[V] = getdata('EN_VELOCITY');
[H] = getdata('EN_HEAD');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% F I G U R E S
figure(1)
plot(Q);  %plot all flows
figure(2)
plot(H(:,2));  %plot all pressures
%close everything
epanetclose();


%------------- END OF CODE --------------
%Please send suggestions for improvement of the above code 
%to Demetrios Eliades at this email address: eldemet@gmail.com.
