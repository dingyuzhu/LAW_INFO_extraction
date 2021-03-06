

# 刑事案件：当qw不为空，但是ssjl为空的切割准则

HEAD_RULE_1 = '\n立案日期|' \
              '\n控辩意见[\S\s]+?\n|' \
              '\n.*?(人民检察院|人民法院|公诉机关).*?指控|' \
              '\n你不服.*?(，|。)|' \
              '\n本院(于|在).*?(，|。)|' \
              '\n你(犯|因犯)|' \
              '\n指控事实|\n指控罪名|\n公诉机关指控情况' \
              '\n本院于[0-9]+?年[0-9]+?月[0-9]+?日|' \
              '\n[0-9]+?年[0-9]+?月[0-9]+?日|\n[0-9]+?月[0-9]+?日|' \
              '\n.*?人民法院.*?作出.*?刑事判决|' \
              '\n判决结果\n|' \
              '\n自诉人.*?以.*?(罪.*?控诉|要求)|' \
              '\n本院收到.*?诉状|' \
              '\n自诉人.*?称：'
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


