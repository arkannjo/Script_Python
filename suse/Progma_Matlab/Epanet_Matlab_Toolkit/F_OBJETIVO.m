function [vajuste, POP] = F_OBJETIVO (ind_pop, f, individuo, ND,NE,DEM)
% F_ONJETIVO - Calcula a função objetivo -----------------------------
%    ind_pop - individuos da população
%          f - matriz de cobertura
%  individuo - Individuos da população (tipo estuturado)
%          ND - Numero de nós da rede
%          NE - numero de estações de monitoramento
%         DEM - vetor de demandas nos nós
%           z - valor máximo provavel
%          FE - fator de escala
%    Veajuste - Veotr com os valores da função objetico da população
%               sem escala
%-----------------------------------------------------------------------
Vetcob = zeros (ND,1);
for i=1:1:ind_pop
     ajust = 0;
    ESTAMON = individuo(i).cromossomo;
 %-----------  Aptidao da população gerada ------------------------------
sumq = 0;
for L =1:1:ND        %Varre as linhas - correspondentes a todos os nós
    soma = 0;
    for C =1:1:NE  %Varre as colunas com as estações de monitoramento
        soma = soma+f(L,ESTAMON(C));
    end
 if soma >= 1      % Verifica se há columa não nula
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
 %---------- Foi excluida a escala da função prevista ------------------
 %                        (ver texto)
 %---------------- Fim da escala de ajuste
end

