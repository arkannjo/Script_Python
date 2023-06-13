function [ f ] = M_FRAC_AGUA( ND, MQ )
	%== M_FRAQ_AGUA Calcula Matriz de fração de água =====================
	%   ND - Numero de nós que compõe a rede 
	%         %numerados sequencial à partir de 1
	%   MQ - Matriz das vazões dos elementos entre os nós (linha e coluna)
	%        que contribue com a vazão para o nó de jusante
	%    f - Retorna ma matriz de fração de água
	% ======================================================================
	f = MQ;              %Cria uma copia matriz de vazao
						 %Que retorna a fração de água
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
	% ------ fim da rotina de obtenção da matriz de fração de agua -----------

end

