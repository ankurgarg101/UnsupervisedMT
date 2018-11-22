python3 preprocess.py  data/mono/vocab.en-fr.600 data/para/dev/newstest2013-ref.en.600  
python3 preprocess.py  data/mono/vocab.en-fr.600 data/para/dev/newstest2013-ref.fr.600  
python3 preprocess.py  data/mono/vocab.en-fr.600 data/para/dev/newstest2014-fren-src.en.600
python3 preprocess.py  data/mono/vocab.en-fr.600 data/para/dev/newstest2014-fren-src.fr.600





python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb True --share_output_emb True --langs 'en,fr' --n_mono -1 --mono_dataset 'en:./data/mono/all.en.tok.600.pth,,;fr:./data/mono/all.fr.tok.600.pth,,' --para_dataset 'en-fr:,./data/para/dev/newstest2013-ref.XX.600.pth,./data/para/dev/newstest2014-fren-src.XX.600.pth' --mono_directions 'en,fr' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2 --pivo_directions 'fr-en-fr,en-fr-en' --lambda_xe_mono '0:1,100000:0.1,300000:0' --lambda_xe_otfd 1 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 100 --stopping_criterion bleu_en_fr_valid,10

# supervised learning
# configurations

python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1 --mono_dataset 'x:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.x.pth,,;y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.y.pth,,' --n_para -1 --para_dataset 'x-y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth'  --para_directions 'x-y' --mono_directions 'x,y' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2 --pivo_directions 'x-y-x,y-x-y' --lambda_xe_mono '0:1,100000:0.1,300000:0'  --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500 --stopping_criterion bleu_x_y_valid,10 --cudnn_enabled False

python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1 --mono_dataset 'x:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.x.pth,,;y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.y.pth,,' --n_para -1 --para_dataset 'x-y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth' --para_directions 'x-y, y-x' --pivo_directions 'x-y-x,y-x-y'   --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_dis 0.5 --n_dis 2 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500 --stopping_criterion bleu_x_y_valid,10 --cudnn_enabled False



# Unpaired and paired dataset (THIS ONE!!!!)
python3 main.py --exp_name test --exp_id results --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1 --mono_dataset 'x:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.x.pth,,;y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.y.pth,,' --n_para -1 --para_dataset 'x-y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth' --mono_directions 'x,y' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2 --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y'   --lambda_xe_mono '0:1,100000:0.1,300000:0' --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_dis 0.5 --n_dis 2 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500 --stopping_criterion bleu_x_y_valid,10 --cudnn_enabled False



# Supervised only on paired dataset (with back translation loss)
python3 main.py --exp_name test --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1 --mono_dataset 'x:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.x.pth,,;y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/unpaired.y.pth,,' --n_para -1 --para_dataset 'x-y:/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth,/home/abhinavds/Documents/Projects/NLP/SemanticParsing/cycle_gan/paired.XX.pth' --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y'   --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_dis 0.5 --n_dis 2 --otf_num_processes 30 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size 500 --stopping_criterion bleu_x_y_valid,10 --cudnn_enabled False

