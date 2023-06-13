function [aux_indiv] = AG (num_est, ND, ind_pop, individuo, prob_mut)
%   AG      - Rotina de algoritimo genetico
%   num_est - numero de estações de monitoramento
%        ND - numero de nos da rede
%   ind_pop - numero de individuos da população
% individuo - vetor de dados dos individuos da popuação
%   prob_mu - probabilidade de mutação
% aux_indiv - Vetor com individuos da nova população
%---------------------------------------------------------------------
 indx = 0;
 while indx < ind_pop
 indx = indx + 1;    
% ----------------- Seleção por torneio ------------------------------
for j = 1:1:2                  %Pais 1 e 2 - seleção
duelante1 = randperm(ind_pop);
duelante2 = randperm(ind_pop);   
for i = 1:1:ind_pop
    if individuo(duelante1(i)).ajuste < individuo(duelante2(i)).ajuste
        pais(j) = individuo(duelante2(i));
    else
        pais(j) = individuo(duelante1(i));
    end
end
end
%-------------------- operador Crossover -----------------------------
part = 1+(num_est-1)*rand;
for im =1:1:num_est         %Cria uma mascara para Cruzamento
    if im < part 
         MASK(im) =  1;
    else
        MASK(im) =  0;;
    end
end;
    for kl = 1:1:num_est
    if MASK(kl) == 1 
    filhos(1).cromossomo(kl) = pais(1).cromossomo(kl);
    filhos(2).cromossomo(kl) = pais(2).cromossomo(kl);
    else
    filhos(1).cromossomo(kl) = pais(2).cromossomo(kl);
    filhos(2).cromossomo(kl) = pais(1).cromossomo(kl);
    end
 end
% --------- verificar se o filho não é defeituoso ----------------------
  for id=1:1:(num_est-1) %verifica se o filho 1 é normal
      for jd = (id+1):1:num_est
     if filhos(1).cromossomo(id) == filhos(1).cromossomo(jd)
           filhos(1).cromossomo = pais(1).cromossomo;
           jd = num_est;
      end
end
  end
  
   for id=1:1:(num_est-1) %verifica se o filho 2 é normal
      for jd =(id+1):1:num_est
      if filhos(2).cromossomo(id) == filhos(2).cromossomo(jd)
           filhos(2).cromossomo = pais(2).cromossomo;
           jd = num_est;
      end
      end
   end
  
%------ cria uma nova população intermediaria de individuos -----------
aux_indiv(indx).cromossomo = filhos(1).cromossomo;
aux_indiv(indx).indice = indx;
aux_indiv(indx).ajuste = 0;
indx = indx+1;
aux_indiv(indx).cromossomo = filhos(2).cromossomo;
aux_indiv(indx).indice = indx;
aux_indiv(indx).ajuste = 0;
end
%---------------------------------------------------------------------- 

%--------------------- Operador Mutação -------------------------------
 for i=1:ind_pop
     for j =1:1:num_est
         if rand < prob_mut
             repetiu = 1;
             while repetiu == 1
                 repetiu = 0;
                 no_aux = round(ND*rand);
                 if no_aux == 0 
                      no_aux = 1;
                 elseif no_aux >= ND
                     no_aux = ND;
                 end
                 for ik=1:1:num_est 
                     if no_aux == aux_indiv(i).cromossomo(ik)
                       repetiu = 1;
                     end
                 end
             end
            aux_indiv(i).cromossomo(j) = no_aux; %gene sofre mutação
         end
     end
  end
end

