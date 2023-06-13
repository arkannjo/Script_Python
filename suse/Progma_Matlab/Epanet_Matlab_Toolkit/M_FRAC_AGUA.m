function [ f ] = M_FRAC_AGUA( ND, MQ )
	%== M_FRAQ_AGUA Calcula Matriz de fra��o de �gua =====================
	%   ND - Numero de n�s que comp�e a rede 
	%         %numerados sequencial � partir de 1
	%   MQ - Matriz das vaz�es dos elementos entre os n�s (linha e coluna)
	%        que contribue com a vaz�o para o n� de jusante
	%    f - Retorna ma matriz de fra��o de �gua
	% ======================================================================
	f = MQ;              %Cria uma copia matriz de vazao
						 %Que retorna a fra��o de �gua
	for L = 1:1:ND;
		Vsoma(L) = 0;
		%Encntra a soma das vazoes para os nos de jusante
		for C=1:1:ND
			Vsoma(L) = Vsoma(L)+MQ(L,C);
		end
	end
	% ----------- fim totalizacao de vazoes aos nos -----------------------

	% --------------- CRIA MATRIZ DE FRA��O DE �GUA ------------------------
	for L=1:1:ND
		for C=1:1:ND
			if Vsoma(L) == 0 
				Vsoma(L)=1;
			end 
			 f(L,C) = MQ(L,C)/Vsoma(L);
		end
	end
	% ---------- Da primeita parte (contribui��o direta)  -------------------
	f = f';  % Trasp�e a matriz de fra��o para forma usual - vide texto
	%---------------------------------------------------------------------
	% Obten�ao dos contribui�oes de n�s indiretamente contribuintes
	% ----------------------------------------------------------------------
	for i = 1:1:ND
		f(i,i) = 1; % fixa o valor 1 na diagonal da matriz de fra��o
	end
	% Inicio do calculo das contribi��es e armazenamento na matriz de fra��o
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
	% ------ fim da rotina de obten��o da matriz de fra��o de agua -----------

end

