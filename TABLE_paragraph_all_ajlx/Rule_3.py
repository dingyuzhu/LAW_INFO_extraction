

# 民事一审判决书头部提取规则
ms_ys_pjs_HEAD_RULE = '\n.{0,5}原告.*?[与诉，]{0,1}被告[\S\s]+?[纠纷争议之诉讼]{2}一案' \
                '|\n原告.[\S\s]{0,10}.*?[纠纷争议之诉]{0,2}一案' \
                '|\n(本院|.*?人民法院).*?[诉与].*?纠纷一案' \
                '|\n上[列述]{1}.[\S\s]{0,20}.*(纠纷|争议).{0,2}案' \
                '|\n.*[与诉]{0,1}.*(纠纷|争议|之诉|诉讼).{0,2}案' \
                '|\n原告.*?(请求|要求)判令：' \
                '|\n判决主文一、' \
                '|\n原、被告[\S\s]+?纠纷一案' \
                '|\n.*?案由.*?\n|\n诉讼请求：'

# 民事一审裁定书头部提取规则
ms_ys_cds_HEAD_RULE = '\n.{0,5}原告.*?[与诉]被告.*?[纠纷]{0,2}.{0,2}案' \
                         '|\n.*?[与诉].*?[纠纷]{0,2}.{0,2}案' \
                         '|\n原告.[\S\s]{0,10}.*?[纠纷]{0,2}.{0,2}案' \
                         '|[\n]{0,1}(本院|.*?人民法院).*?[诉与]{0,1}.*?纠纷一案' \
                         '|\n(上列|以上|上述).[\S\s]{0,20}.*(纠纷|争议)一案' \
                         '|\n本院.*?[审办受]理.*?[纠纷一案]{0,4}(中|过程中)' \
                         '|\n本院于[0-9]+年[0-9]+月[0-9]+[日]{0,1}.*?裁定' \
                         '|\n[0-9]+年[0-9]+月[0-9]+日' \
                         '|\n本院收到.*?诉状' \
                         '|\n原告[起]{0,1}诉称.[\S\s]+.*?本院认为' \
                         '|^((?!：).)*申请人.*?纠纷一案((?!：).)*$' \
                         '|\n申请人.*?提出.*?申请' \
                         '|\n.{0,3}(申请人|原告|本院).*?(财产保全|先于执行)' \
                         '|\n原.*?被.*?纠纷一案' \
                         '|\n本院于.*?作出[\S\s]+?裁定' \
                         '|\n起诉人.*?称'


# 民事一审调解书头部提取规则
ms_ys_tjs_HEAD_RULE ='\n原告.*?[与诉]被告.*?[纠纷]{0,2}.{0,2}案' \
                '|[\n]{0,1}(本院|.*?人民法院).*?[诉与]{0,1}.*?[纠纷]{0,2}一案' \
                '|\n(上列|以上|上述).[\S\s]{0,20}.*(纠纷|争议)一案' \
                '|\n案由[：]{0,1}.*?[纠纷]{0,2}[\s]{1}' \
                '|\n原告.[\S\s]{0,10}.*?[纠纷]{0,2}.{0,2}案'

#民事二审判决书头部提取规则
ms_es_pjs_HEAD_RULE = '((?!：).)*上诉人.*?与[被上诉人]{0,4}.*?纠纷.{0,2}案((?!：).)' \
                '|\n.{0,3}(上诉人|原审原告|原告)[^：].*?[纠纷争议]{0,2}一案' \
                '|\n(上诉人|原审原告)[^：].*?合同纠纷' \
                '|\n.*?[与诉]{1}.*?[争议纠纷]{0,2}.*?案' \
                '|\n.*?本案现已审理终结。' \
                '|\n上诉请求及事实和理由'


#民事二审裁定书头部提取规则
ms_es_cds_HEAD_RULE ='\n(申请再审人|再审申请人|.*).*?不服[\S\s]+?(提起上诉|申请再审|再审申请|进行再审)' \
                '|[\n]{0,1}(再审申请人|原审原告|申诉人|原告|一审原告).*?[诉与]{1}(被申请人|原审被告|被申诉人|被告|一审被告).*?[纠纷]{0,2}一案' \
                '|\n.*?[与诉]{0,1}.*?纠纷一案'


#民事再审裁定书头部提取规则
ms_zs_cds_HEAD_RULE ='\n(申请再审人|再审申请人|.*).*?不服[\S\s]+?(提起上诉|申请再审|再审申请|进行再审)' \
                    '|[\n]{0,1}(再审申请人|原审原告|申诉人|原告|一审原告).*?[诉与]{1}(被申请人|原审被告|被申诉人|被告|一审被告).*?[纠纷]{0,2}一案' \
                    '|\n.*?[与诉]{0,1}.*?纠纷一案'





#提取诉讼请求的规则1
SSQQ_Rule = '[变更]*.{0,2}(变更|请求|诉请).{0,2}[\S\s]+?事实[与及和]{1}理由[为]{0,1}.*?(：|:|，)|' \
                         '[变更]*.{0,2}(变更|请求|诉请).{0,2}(:|：)[\S\s]+?\n|' \
                         '(诉请|诉讼请求[为]{0,1}|请求)(:|：|\n)[\S\s]+?。|' \
                         '(请求|要求|诉请).{0,8}(判令|判决|改判).{0,3}(：|:)[\S\s]+?。|' \
                         '[\S\s]+?事实[与及和]{1}理由[为]{0,1}.*?(：|:|，)|' \
                         '((诉|状|诉请|诉讼|起诉)[至来].{0,4}[法本贵我]院|故到贵院起诉|故起诉到法院).*?(要求|请求|判令)[\S\s]+?。|' \
                         '(现起诉要求|现依法起诉|提起诉讼)[\S\s]+?。|' \
                         '向.*?(法院|本院|贵院).*?(诉讼|起诉|申请|请求).*?(要求|请求|申请)[\S\s]+?。|' \
                         '(请求|诉请)(人民法院：|本院|法院|人民法院)[\S\s]+?。|' \
                         '请求.*?(判决|判令)被告[\S\s]+?。|' \
                         '(要求|诉请)[\S\s]*?(被告|被申请人|被上诉人|被申诉人)[\S\s]*?(支付|退还|赔偿|赔付|返还|偿还)[\S\s]*?。|' \
                         '(诉称|请求|诉请|请求)[\S\s]{0,20}?(判令)[\S\s]*?。|' \
                         '(申请|请求).{0,10}(再审[称]|主要称).*?(，|:|：)|(申请|请求).{0,10}(再审|撤销).*?。|' \
                         '(上诉人|原告).*?申请撤回.*?上诉|(上诉人|原告|).*?(撤诉申请|撤回上诉)|.*?撤回上诉.*?(申请|请求)|(上诉人|原告)*?撤诉|申请撤回[上起]诉|申请撤诉|审理过程中.*?撤回.*?上诉|' \
                         '(申请|请求).{0,5}撤销.*?(仲裁|裁决).*?。|' \
                         '(请求|要求).*?确认.*?一案|(请求|要求).*?(确认|宣告).*?。|(请求|申请|要求).*?(法院|依法)认定.*?。|(请求|申请|要求)[\S\s]+?(认定|宣告).*?。|' \
                         '要求.*?(被告|被申请人|被上诉人|被申诉人)[\S\s]+?。|' \
                         '申请解除[\S\s]+?。|' \
                         '[现故特]{1}.{0,2}(申请|要求|请求)[\S\s]+?。|' \
                         '请求(判决|依法)[\S\s]+?。|' \
                         '(原告|，)(申请|要求|请求)[\S\s]+?。'



#提取诉讼请求的规则2
SSQQ_Rule_ ='[变更]*.{0,2}(变更|请求|诉请).{0,2}(:|：)[\S\s]+|' \
                 '(诉请|诉讼请求[为]{0,1}|请求)(:|：|\n)[\S\s]+|' \
                 '(请求|要求|诉请).{0,8}(判令|判决|改判).{0,3}(：|:)[\S\s]+|' \
                 '((诉|状|诉请|诉讼|起诉)[至来].{0,4}[法本我]院|故到贵院起诉|故起诉到法院).*?(要求|请求|判令)[\S\s]+|' \
                 '(现起诉要求|现依法起诉|提起诉讼)[\S\s]+[\S\s]+|' \
                 '向.*?(法院|本院|贵院).*?(诉讼|起诉|申请|请求).*?(要求|请求|申请)[\S\s]+|' \
                 '(请求|诉请)(人民法院：|本院|法院|人民法院)[\S\s]+|' \
                 '请求.*?(判决|判令)被告[\S\s]+|' \
                 '(要求|诉请)[\S\s]*?(被告|被申请人|被上诉人|被申诉人)[\S\s]*?(支付|退还|赔偿|赔付|返还|偿还)[\S\s]*|' \
                 '(诉称|请求|诉请|申请)[\S\s]{0,20}?(判令)[\S\s]*|' \
                 '(申请|请求).{0,10}(再审[称]{0,1}|主要称).*?(，|:|：)|(申请|请求).{0,10}(再审|撤销).*|' \
                 '(上诉人|原告).*?申请撤回.*?上诉|(上诉人|原告|).*?(撤诉申请|撤回上诉)|.*?撤回上诉.*?(申请|请求)|(上诉人|原告)*?撤诉|申请撤回[上起]诉|申请撤诉|审理过程中.*?撤回.*?上诉|' \
                 '(申请|请求).{0,5}撤销.*?(仲裁|裁决).*|' \
                 '(请求|要求).*?确认.*?一案|(请求|要求).*?(确认|宣告).*|(请求|申请|要求).*?(法院|依法)认定.*|(请求|申请|要求)[\S\s]+?(认定|宣告).*|' \
                 '要求.*?(被告|被申请人|被上诉人|被申诉人)[\S\s]+|' \
                 '申请解除[\S\s]+|' \
                 '[现故特]{1}.{0,2}(申请|要求|请求)[\S\s]+|' \
                 '请求(判决|依法)[\S\s]+|' \
                 '(原告|，)(申请|要求|请求)[\S\s]+'
