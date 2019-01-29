def __score(standard: str, tester: str):
    score = 0
    sub_index = 0
    tolerance = 3
    for si, s in enumerate(standard):
        for i, t in enumerate(tester[sub_index:]):
            if s == t:
                score += 1
                sub_index = sub_index + i
                break
            if si != 0 and i >= tolerance:
                break

    return score / len(standard)


def match_index(headers: list, texts: list):
    minimum_score = .7
    scores = [0. for _ in range(len(texts))]
    texts = list(map(lambda _: _[:50], texts))
    for header_idx, header in enumerate(headers):
        for text_idx, text in enumerate(texts):
            # if header['name'] == '询问笔录' and text_idx == 97:
            #     print('##################')

            score = __score(header['name'], text)
            # score = fuzz.token_sort_ratio(text, header['name'])
            if score > max(scores[header_idx], minimum_score):
                header['start'] = text_idx
                header['text'] = text
                scores[text_idx] = score
    return headers


if __name__ == '__main__':
    _texts = ['', '起诉书津巾捻诉删诉【20！8J632号被告人毛有良，男t984年！！月！！日出生，公民身份号码:62',
              '而后将赃款藏匿在其居住的d、区二废弃冰箱内并将用于伪的衣物遗弃。2018年5月22日民警将被告人毛有', '此致天津市南开区人民法院附:助缪',
              '时间:o饰8月；g日地点:隋茵签发人:焱袭向:被告人姓名、年龄、籍贯、捕前职业、住址等，并告知其如不',
              '时间:2018年$月lG日签发人:$8狱Py8问:被告人3弥的政治面貌是什么?问:你的组织关系在哪里', '', '', '',
              '认罪认罚具结书一、犯罪嫌疑人身份信息杏人姓名二、权利知悉本人已阅读《认非认衍从觉$！戊台A！！战》G',
              '本《认罪认罚具结书》，是本人在知情和自愿的情况下签署，未受任何暴力、威胁或任何其他形式的非法影响，亦', '', '', '', '',
              '案由:盗窃开庭时间:二0二/\\年/\\月十-上日十时丕十曰三十分录像时间:二0二/\\年，V月！土日十时',
              '动进行录音、录像、摄影，或者通过发送邮件、博客、彼博客等方式传播庭审情况；(四)不得发言、提问；(五',
              '审:本次因何、在何时被采取强制措施?答:2018年5月22日因涉嫌盗窃罪被天津市公安局南开分局刑事拘',
              '答:同意。审:干津市南开区人民法院刑事审判庭今夭依法公开审理被告人毛有良盗窃二案，杏法庭由审判员朱颍',
              '审判员:现在开始法庭事实调查。审判员:首先由公诉人宣读起诉书。公诉人:宣读起诉书(内容略)。审判员:',
              '出示视听资料(略)；出示文件检验鉴定书(略)i出示被告人毛有良的悔过书及其供述(略)。审判员:被告人',
              '审判员；被告人毛有良起立。现在由被告人向法庭作最后陈述。被告人:本认罪认罚，希望法庭从轻处罚。审判员',
              '量刑建议书津巾捻公诉喜建【2018J755号被告人上涉嫌缕二案，在院以蕊莹起诉书问你院提起公诉，经审', '', '天津市岗开区人战燊删耳判逃l；(20！8)；P0！04肛’！初s7I号',
              '伪装成女子，至本市南开区时代奥城商业广场阿依来新疆。城店，潜入餐厅三楼办公室后用钥匙打开保险柜、用菜',
              '被告人毛有良犯盗窃罪，判处拘役三个月，并处罚金3000(刑期从判处执行之日起计算；判决执行以前先行羁',
              '附:在裁判文书所依据法律规定的具体条文《中华人民共和国刑法》第二百六十四条盗窃公私财物，数额较大的，', '刑事案件宣判笔录沄二午一时', '', '', '', '', '', '(袋案镒用',
              '陋开区肴C所释放证阴书(刚个)津公南胥释字“8J，', '夭淇市公安局峨分扇释放通剑书津公(南开)释字rcU！9及', '', '(e案卷通用)', '',
              '夭津荫岗爪区人战燊刷冉判火l；C20！8)；甘0！！Jq#l！初玉7！呈', '尹。5。兢f5。。a。5占。。。“。兢肌。n桌抽屉锁盗走现金18248元，后将赃款藏匿在其居住的d、',
              '被告人毛有良犯盗窃罪，判处拘役三个月，并处罚金3000(刑期从判处执行之日起计算；判决执行以前先行羁',
              '附:本裁判文书所依据法律规定的具体条文《中华人民共和国刑法》第二百六十四条盗窃公私财物，数额较大的，', '', '', '', '', '', '', '',
              '津开公(法)提捕守120！8j纱号犯罪嫌疑人毛有良，男，33岁，1984年1！月1i日出生，汉族，政',
              '综上犯罪嫌疑人毛有良的行为，触犯了《中华人民共和国刑法》第二百六十四条之规定，涉嫌盗窃罪。其行为有可', '', '', '', '',
              '4、案情摘要:2018年5月2！日珏津市南开区时代奥塬商业广场C！来新疆餐厅盗窃案j、检材和样在:', '', '', 'd须’芷上', '', 'da！立上',
              '天津市公安局南开分局鉴定意见通知书(副本)津开公(刑)鉴通字(20！8)0i5我局“有关人员烜付一进',
              '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final/',
              '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final/', '', '勘验人员:', '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '', '', '', '', '', '', '', '间咎年s月绞日3时“至纱年s月g日3时。查人员姓名、单位录人姓名、单位事人:证人:',
              '', '', '', '', '', '', '询问笔录“目绞曰衅伞分贫纱da纠l！丝时缎分人(签名)“、邀！作悦价人(签名)一千作详位问“性别红i', '', '', '', '',
              'wa绞日旦时旦分爷咎年旦丝l！旦时旦分问人“别终年龄巡宓！！！牛！！W证件种类及；呜门！熟人人代衣', '', '', '',
              '时间纱年6月4日9时旦分至咎年6月4日旦时纱询问地点-询问人(签名)验、工作单位记录员(签名)垃工作', '', '',
              '“等a纤P旦时骅介萃“a红l旦时m人(签名)线、“-P作乌仙人(签名)“I你甲位问人岱KF兄V丛乙上', '610i24i980！lll0333。', '',
              '时间纱年6月4日旦时但分至咎年6月4日！时巡分询问地点询问人(签名)验、壁工作单位记录员(签名)垃工', '',
              '间逍5月旦日旦时分至纱年5月旦日纱时纱问人(签名)“、“工作单位人(签名)垃工作单位问人乎性别女年龄', '', '', 'v，g‘q乙，！！', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '2018年5月21日，报警人柳d、娟报称:2018年5月2！日8时40分左右，其发现天津市颜开区它水', '',
              '2018年5月21H8时46分，我所接llO指挥中，心派瞥，称在夭潇市南开区宾水西道时代奥城Cl区阿',
              '2018年5月21日8时46分，我所接1！0指挥中‘心派瞥，称在夭津市南开区宾水西道时代奥城C！区阿',
              '2018年5月2！日8时46分，我所接！10指挥中‘心派警，称在天津市南开区宾水西道时代奥城C！区阿', '人员动态管控网、TCIC、比对毛有良，未发现有违法犯罪记', '',
              '耳记鹄甘肃省庆阳高凹蹬战$W乡E过胄卜汾队！！它衅甘肃谷庆阳！h凹蹬战tt肃谷戊阳m缆懒！“状“它$', '！/！1/！示?条v*', '', '', '辙“空$', '', '', '', '',
              '黏$g卫5津刺商开区阿依米熊厂职务:店长证件脊型；身价i！F身份证口码:o！O！aq！980！！！！', '', '', '侦查员姓名、单位记求员岱Y位弋一犯非嫌疑人-一-一s“丝！然衅', '',
              '上岱d阶%I！?！！', '上一蚁！?8--一-一w?一--一-一', '记录员璘单位犯非嫌疑人旻“-燊剑t隙怠一上公什i:燃:?3g！Ph:cw', '', '',
              'l！CkVVP！:?燕你垃！线一一一-一', '----一小%；驳%A价VY必！么，8i；线“', '侦查员姓名、单位记求员旻单位犯鼎嫌疑人iV%Q-！俭愿Wi慕',
              '-一一--一------一一一--一-', '讯问笔录晌纱年旦月丝日旦时线至“年旦月g日壁时g讯问人(签名)“、w作单位上记录人(签名)“工作单位', '', '', '', '', '',
              '讯问笔录时间丛年乏月驾日！m至驾年红月二日乙时乓讯问人(签名)“、“作单记录人(签名)燊工作单位被讯', '',
              '讯问笔录珈“g月马旦时丝至“年目a呜时。问人(签名)“、a工作单位记录人(签名)兰工作单位讯问人璧性', '', '', '', '', '', '骝讯问笔录身继件种类及号码一C是“人大代表',
              '', '', '', '']

    _headers = [{'name': '监控录像截图', 'start': None}, {'name': '调取证据清单', 'start': None},
                {'name': '计算机司法鉴定意见', 'start': None}, {'name': '搜查笔录、扣押笔录、扣押清单', 'start': None},
                {'name': '受案登记表', 'start': None}, {'name': '足迹鉴定书', 'start': None},
                {'name': '书面报案材料', 'start': None}, {'name': '赃证物品照片', 'start': None},
                {'name': '电子数据检验报告', 'start': None}, {'name': '公安业务档案卡', 'start': None},
                {'name': '现场勘验笔录', 'start': None}, {'name': '价格认定结论书', 'start': None},
                {'name': '常住人口基本信息', 'start': None}, {'name': '询问笔录', 'start': None},
                {'name': '辨认笔录', 'start': None}, {'name': '工作情况', 'start': None}, {'name': '刑事裁定书', 'start': None},
                {'name': '释放证明', 'start': None}, {'name': '营业执照', 'start': None}, {'name': '指纹鉴定书', 'start': None},
                {'name': '讯问笔录', 'start': None}, {'name': 'DNA鉴定书', 'start': None},
                {'name': '远程勘验笔录', 'start': None}, {'name': '财产损失证明', 'start': None},
                {'name': '刑事判决书', 'start': None}, {'name': '行政处罚决定书', 'start': None},
                {'name': '认罪认罚具结书', 'start': None}, {'name': '手机、GPS轨迹及情况说明', 'start': None}]

    _headers = match_index(_headers, _texts)
    pass
    # scr = __score('刑事判决书', '肆市妍区氏晞刑事判决！；(20！8)；丰0104刑初57！号公诉机关天津市南#区人续检%院被告人毛有良男、！98q咎！！6:！！iigig肃省庄F己页、民身份号码62280！！984！！！！！8！$；《8、8！汶?Y:千；肆莎菊')
    # scr = __score('询问笔录', '询问笔录“目绞曰衅伞分贫纱da纠l！丝时缎分人(签名)“、邀！作悦价人(签名)一千作详位问“性别红i龄验珍！！i/上！！！VJ证件种类及！j绶O；！ci人太(V冬')
    # print(scr)
