function [vajuste, POP] = F_OBJETIVO (ind_pop, f, individuo, ND,NE,DEM)
% F_ONJETIVO - Calcula a fun��o objetivo -----------------------------
%    ind_pop - individuos da popula��o
%          f - matriz de cobertura
%  individuo - Individuos da popula��o (tipo estuturado)
%          ND - Numero de n�s da rede
%          NE - numero de esta��es de monitoramento
%         DEM - vetor de demandas nos n�s
%           z - valor m�ximo provavel
%          FE - fator de escala
%    Veajuste - Veotr com os valores da fun��o objetico da popula��o
%               sem escala
%-----------------------------------------------------------------------
Vetcob = zeros (ND,1);
for i=1:1:ind_pop
     ajust = 0;
    ESTAMON = individuo(i).cromossomo;
 %-----------  Aptidao da popula��o gerada ------------------------------
sumq = 0;
for L =1:1:ND        %Varre as linhas - correspondentes a todos os n�s
    soma = 0;
    for C =1:1:NE  %Varre as colunas com as esta��es de monitoramento
        soma = soma+f(L,ESTAMON(C));
    end
 if soma >= 1      % Verifica se h� columa n�o nula
 Vetcob (L) = 1;
 else
 Vetcob(L) = 0;
 end
 VCD(L) = Vetcob(L)*DEM(L);
 sumq = sumq + VCD(L);
end
    FR = sumq;         %substituiu FR = 100-((z-sumq)/z*100);
    vajuste(i) = FR;
end
 
  for i=1:1:ind_pop
   individuo(i).ajuste = vajuste(i);
  end
  POP = individuo;
 %---------- Foi excluida a escala da fun��o prevista ------------------
 %                        (ver texto)
 %---------------- Fim da escala de ajuste
end

