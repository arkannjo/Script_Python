function [FF] = MAT_COBERTURA(ND, f, criterio)
%MAT_COBERTURA - Obtem A matriz de cobertura associada a f
%   Sendo: ND numero de n�s na rede hidr�ulica (dimens�o NDXND de f)
%          f - Matriz de fra��o de vaz�o -> Matriz de cobertura FF
%          criterio - percentagem da vazao total coberta
%-------------------------------------------------------------------
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

end

