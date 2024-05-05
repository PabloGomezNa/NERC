#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse

from deptree import *
#import patterns


## ------------------- 
## -- Convert a pair of drugs and their context in a feature vector

def extract_features(tree, entities, e1, e2) :
   feats = set()

   # print("ENTITIES:",entities,"ENTITY ONE", e1,"ENTITY TWO", e2)
   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   # print("TKE1",tkE1, "TKE2",tkE2)

   if tkE1 is not None and tkE2 is not None:
      # features for tokens in between E1 and E2
      #for tk in range(tkE1+1, tkE2) :
      tk=tkE1+1
      try:
        while (tree.is_stopword(tk)):
          tk += 1
      except:
        return set()
      word  = tree.get_word(tk)
      lemma = tree.get_lemma(tk).lower()
      tag = tree.get_tag(tk)
      feats.add("lib=" + lemma)
      feats.add("wib=" + word)
      feats.add("lpib=" + lemma + "_" + tag)
      
      eib = False
      for tk in range(tkE1+1, tkE2) :
         if tree.is_entity(tk, entities):
            eib = True 
      
	  # feature indicating the presence of an entity in between E1 and E2
      feats.add('eib='+ str(eib))

      # features about paths in the tree
      lcs = tree.get_LCS(tkE1,tkE2)

      # 6 LCS tag/rel/word/lemma
      feats.add("lcs_tag="+tree.get_tag(lcs))
      feats.add("lcs_rel="+tree.get_rel(lcs))
      feats.add("lcs_word="+tree.get_word(lcs))
      feats.add("lcs_lemma="+tree.get_lemma(lcs))
      
      # 7 Path with Tag // 8 Path with Rel // 9 Path with Lemma // 10 Path with Tag and Rel

      pathorig1 = tree.get_up_path(tkE1,lcs)
      path1 = "<".join([tree.get_lemma(x)+"_"+tree.get_rel(x) for x in pathorig1])
      path_tag1 = "<".join([tree.get_tag(x) for x in pathorig1])
      path_lemma1 = "<".join([tree.get_lemma(x) for x in pathorig1])
      path_rel1 = "<".join([tree.get_rel(x) for x in pathorig1])
      path_rel_tag1 = "<".join([tree.get_rel(x)+"_"+tree.get_tag(x) for x in pathorig1])

      feats.add("path1="+path1)
      feats.add("path_tag1="+path_tag1)
      # feats.add("path_lemma1="+path_lemma1)
      # feats.add("path_rel1="+path_rel1)
      # feats.add("path_rel_tag1="+path_rel_tag1)

      pathorig2 = tree.get_down_path(lcs,tkE2)
      path2 = ">".join([tree.get_lemma(x)+"_"+tree.get_rel(x) for x in pathorig2])
      path_tag2 = ">".join([tree.get_tag(x) for x in pathorig2])
      path_lemma2 = ">".join([tree.get_lemma(x) for x in pathorig2])
      path_rel2 = ">".join([tree.get_rel(x) for x in pathorig2])
      path_rel_tag2 = ">".join([tree.get_rel(x)+"_"+tree.get_tag(x) for x in pathorig2])

      feats.add("path2="+path2)
      feats.add("path_tag2="+path_tag2)
      # feats.add("path_lemma2="+path_lemma2)
      # feats.add("path_rel2="+path_rel2)
      # feats.add("path_rel_tag2="+path_rel_tag2)

      path = path1+"<"+tree.get_lemma(lcs)+"_"+tree.get_rel(lcs)+">"+path2
      path_tag = path_tag1+"<"+tree.get_tag(lcs)+">"+path_tag2 
      path_lemma = path_lemma1+"<"+tree.get_lemma(lcs)+">"+path_lemma2  
      path_rel = path_rel1+"<"+tree.get_rel(lcs)+">"+path_rel2   
      path_rel_tag = path_rel_tag1+"<"+tree.get_rel(lcs)+"_"+tree.get_tag(lcs)+">"+path_rel_tag2  

      feats.add("path="+path)
      feats.add("path_tag="+path_tag)
      # feats.add("path_lemma="+path_lemma)
      # feats.add("path_rel="+path_rel)
      # feats.add("path_rel_tag="+path_rel_tag)


      # 11 Direct / Indirect relation
      # if len(pathorig1)+len(pathorig2)<4:
      #    feats.add("direct_encoded=direct")
      # else:
      #    feats.add("direct_encoded=indirect")

     

    

      #1 Clue verbs // 2 Clue verbs position

      clue_verbs_effect=['tendency','stimulate','regulate','prostate','modification','accentuate','exacerbate','diminish','augment','exhibit','experience','counteract','potentiate','enhance','reduce','antagonize']
      clue_verbs_mechanism=['impair','inhibit','displace','accelerate','bind','induce','decrease','elevate','delay','react','faster','presumably','induction','substantially','minimally']
      clue_verbs_advise=['exceed','extreme','cautiously']
      clue_verbs_int=['suggest', 'interact']

      clue_verbs_found_effect = 0
      clue_verbs_found_mechanism = 0
      clue_verbs_found_advise = 0
      clue_verbs_found_int = 0


      # cv_effect_position='0'
      # cv_mechanism_position='0'
      # cv_advise_position='0'
      # cv_int_position='0'


      for node_id in tree.get_nodes():
         lemma = tree.get_lemma(node_id)
         if lemma in clue_verbs_effect:
               clue_verbs_found_effect=1

               # if node_id<int(tkE1):
               #    cv_effect_position="before"                
               # elif int(tkE1)<node_id and node_id<int(tkE2):
               #    cv_effect_position="mid"
               # else:
               #    cv_effect_position="after"
         if lemma in clue_verbs_mechanism:
               clue_verbs_found_mechanism=1

               # if node_id<int(tkE1):
               #    cv_mechanism_position="before"
               # elif int(tkE1)<node_id and node_id<int(tkE2):
               #    cv_mechanism_position="mid"
               # else:
               #    cv_mechanism_position="after"
         if lemma in clue_verbs_advise:
               clue_verbs_found_advise=1

               # if node_id<int(tkE1):
               #    cv_advise_position="before"
               # elif int(tkE1)<node_id and node_id<int(tkE2):
               #    cv_advise_position="mid"
               # else:
               #    cv_advise_position="after"
         if lemma in clue_verbs_int:
               clue_verbs_found_int=1

               # if node_id<int(tkE1):
               #    cv_int_position="before"
               # elif int(tkE1)<node_id and node_id<int(tkE2):
               #    cv_int_position="mid"
               # else:
               #    cv_int_position="after"
      
      # if cv_effect_position!='0':
      #    feats.add("cv_effect_position=" + cv_effect_position )
      
      # if cv_mechanism_position!='0':
      #    feats.add("cv_mechanism_position=" + cv_mechanism_position )

      # if cv_advise_position!='0':
      #    feats.add("cv_advise_position=" + cv_advise_position )

      # if cv_int_position!='0':
      #    feats.add("cv_int_position=" + cv_int_position )


      feats.add("clue_verbs_effect=" + str(clue_verbs_found_effect) )
      feats.add("clue_verbs_mechanism=" + str(clue_verbs_found_mechanism) )
      feats.add("clue_verbs_advise=" + str(clue_verbs_found_advise) )
      feats.add("clue_verbs_int=" + str(clue_verbs_found_int) )

      # 3 Word/Lemma/PoS of context words
      # Words, lemmas, PoS tags appearing before/in-between/after the target pair
      # Before 1
      words_before = tree.get_word(int(tkE1)-1) 
      lemmas_before = tree.get_lemma(int(tkE1)-1).lower()
      pos_before = tree.get_tag(int(tkE1)-1) 

      if(len(words_before)!=0 and words_before!="<none>"):
         feats.add("word_before=" + words_before )
         feats.add("lemma_before=" +  lemmas_before)
         feats.add("pos_before=" + pos_before)


      # Before 2
      if tkE1>1:
         words_before = tree.get_word(int(tkE1)-2) 
         lemmas_before = tree.get_lemma(int(tkE1)-2).lower()
         pos_before = tree.get_tag(int(tkE1)-2)

         if(len(words_before)!=0 and words_before!="<none>"):
            feats.add("word_before2=" + words_before )
            feats.add("lemma_before2=" +  lemmas_before)
            feats.add("pos_before2=" + pos_before)


      # Before 3
      if tkE1>2:
         words_before = tree.get_word(int(tkE1)-3) 
         lemmas_before = tree.get_lemma(int(tkE1)-3).lower()
         pos_before = tree.get_tag(int(tkE1)-3)

         if(len(words_before)!=0 and words_before!="<none>"):
            feats.add("word_before3=" + words_before )
            feats.add("lemma_before3=" +  lemmas_before)
            feats.add("pos_before3=" + pos_before)

      
      # Before 4
      if tkE1>3:
         words_before = tree.get_word(int(tkE1)-4) 
         lemmas_before = tree.get_lemma(int(tkE1)-4).lower()
         pos_before = tree.get_tag(int(tkE1)-4) 

         if(len(words_before)!=0 and words_before!="<none>"):
            feats.add("word_before4=" + words_before )
            feats.add("lemma_before4=" +  lemmas_before)
            feats.add("pos_before4=" + pos_before)


      # Between
      for tk in range((tkE1 + 1),(tkE2)):
         if tk<= (tkE1+4):
            feats.add("word_between_post"+ str(tk-(tkE1+1)) +"=" +tree.get_word(tk))
            feats.add("lemma_between_post"+ str(tk-(tkE1+1)) +"=" +tree.get_lemma(tk))
            feats.add("pos_between_post"+ str(tk-(tkE1+1)) +"=" +tree.get_tag(tk))

         if tk>=(tkE2-4):
            feats.add("word_between_pre"+ str(tk-(tkE2-3)) +"=" +tree.get_word(tk))
            feats.add("lemma_between_pre"+ str(tk-(tkE2-3)) +"=" +tree.get_lemma(tk))
            feats.add("pos_between_pre"+ str(tk-(tkE2-3)) +"=" +tree.get_tag(tk))
 

      # After
      if(tree.get_n_nodes()-1>tkE2):
         words_after = tree.get_word(int(tkE2)+1)
         lemmas_after = tree.get_lemma(int(tkE2)+1)
         pos_after = tree.get_tag(int(tkE2)+1)

      else: 
         words_after=""      
      if(len(words_after)!=0 and words_after!="<none>"):
         feats.add("word_after=" + words_after)
         feats.add("lemma_after=" +  lemmas_after)
         feats.add("pos_after=" + pos_after)



      # After2
      if(tree.get_n_nodes()-1>tkE2+1):
         words_after = tree.get_word(int(tkE2)+2)
         lemmas_after = tree.get_lemma(int(tkE2)+2)
         pos_after = tree.get_tag(int(tkE2)+2)

      else: 
         words_after=""      
      if(len(words_after)!=0 and words_after!="<none>"):
         feats.add("word_after2=" + words_after)
         feats.add("lemma_after2=" +  lemmas_after)
         feats.add("pos_after2=" + pos_after)



      # After3
      if(tree.get_n_nodes()-1>tkE2+2):
         words_after = tree.get_word(int(tkE2)+3)
         lemmas_after = tree.get_lemma(int(tkE2)+3)
         pos_after = tree.get_tag(int(tkE2)+3)

      else: 
         words_after=""      
      if(len(words_after)!=0 and words_after!="<none>"):
         feats.add("word_after3=" + words_after)
         feats.add("lemma_after3=" +  lemmas_after)
         feats.add("pos_after3=" + pos_after)


      # After4
      if(tree.get_n_nodes()-1>tkE2+3):
         words_after = tree.get_word(int(tkE2)+4)
         lemmas_after = tree.get_lemma(int(tkE2)+4)
         pos_after = tree.get_tag(int(tkE2)+4)

      else: 
         words_after=""      
      if(len(words_after)!=0 and words_after!="<none>"):
         feats.add("word_after4=" + words_after)
         feats.add("lemma_after4=" +  lemmas_after)
         feats.add("pos_after4=" + pos_after)

      

      # 4 Distance Between entities


      # if int(tkE2)-int(tkE1) < 10:
      #    feats.add("distance=small")
      # else:
      #    feats.add("distance=large")

      # 5 Offset span

      # right,left=tree.get_subtree_offset_span(tkE1)
      # if right>3:
      #    feats.add("tk1_right=large")
      # else:
      #    feats.add("tk1_right=small")
      
      # if left>3:
      #    feats.add("tk1_left=large")
      # else:
      #    feats.add("tk1_left=small")
      

      # right,left=tree.get_subtree_offset_span(tkE2)
      # if right>3:
      #    feats.add("tk2_right=large")
      # else:
      #    feats.add("tk2_right=small")
      
      # if left>3:
      #    feats.add("tk2_left=large")
      # else:
      #    feats.add("tk2_left=small")
      # feats.add("tk2_right=" + str(right))
      # feats.add("tk2_left=" + str(left))

      #Parent node characteristics
      # parente1=tree.get_parent(tkE1)
      # feats.add("parent1_tag="+tree.get_tag(parente1))
      # feats.add("parent1_word="+tree.get_word(parente1))
      # feats.add("parent1_lemma="+tree.get_lemma(parente1))
      # feats.add("parent1_rel="+tree.get_rel(parente1))
      # parente2=tree.get_parent(tkE2)
      # feats.add("parent2_tag="+tree.get_tag(parente2))
      # feats.add("parent2_word="+tree.get_word(parente2))
      # feats.add("parent2_lemma="+tree.get_lemma(parente2))
      # feats.add("parent2_rel="+tree.get_rel(parente2))


      # if tree.get_n_nodes()>20:
      #    feats.add("len=large")
      # else:
      #    feats.add("len=short")

      # ancestorse1=set(tree.get_ancestors(tkE1))
      # ancestorse2=set(tree.get_ancestors(tkE2))

      # common_ancestors = ancestorse1.intersection(ancestorse2)
      # feats.add("num_com_ancestors="+str(len(common_ancestors)))




      

   return feats


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  extract_features targetdir
## --
## -- Extracts feature vectors for DD interaction pairs from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :

    # parse XML file, obtaining a DOM tree
    tree = parse(datadir+"/"+f)

    # process each sentence in the file
    sentences = tree.getElementsByTagName("sentence")
    for s in sentences :
        sid = s.attributes["id"].value   # get sentence id
        stext = s.attributes["text"].value   # get sentence text
        # load sentence entities
        entities = {}
        ents = s.getElementsByTagName("entity")
        for e in ents :
           id = e.attributes["id"].value
           offs = e.attributes["charOffset"].value.split("-")           
           entities[id] = {'start': int(offs[0]), 'end': int(offs[-1])}

        # there are no entity pairs, skip sentence
        if len(entities) <= 1 : continue

        # analyze sentence
        analysis = deptree(stext)

        # for each pair in the sentence, decide whether it is DDI and its type
        pairs = s.getElementsByTagName("pair")
        for p in pairs:
            # ground truth
            ddi = p.attributes["ddi"].value
            if (ddi=="true") : dditype = p.attributes["type"].value
            else : dditype = "null"
            # target entities
            id_e1 = p.attributes["e1"].value
            id_e2 = p.attributes["e2"].value
            # feature extraction

            feats = extract_features(analysis,entities,id_e1,id_e2)
            # resulting vector
            if len(feats) != 0:
              print(sid, id_e1, id_e2, dditype, "\t".join(sorted(feats)), sep="\t")
