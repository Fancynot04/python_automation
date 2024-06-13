/*********************************
 * Themes, rules, and i18n support
 * Locale: Chinese; 中文
 * function: 1.Basic logic for checking if a numeric string falls within a specified  
 *           range
 *           2.The three types of validation for input data are basic validation,
 *           logical validation,cross-table validation 
 *********************************/
(function(factory) {
    typeof module === "object" && module.exports ? //
        module.exports = factory(require("jquery")) : //
        typeof define === "function" && define.amd ? define(["jquery"], factory) : factory(jQuery);
}(function($) {

    /* Global configuration
     */
    $.validator.config({
        //stopOnError: true,
        //focusCleanup: true,
        //theme: 'yellow_right',
        //timely: 2,

        // Custom rules
        rules: {
            digits: [/^\d+$/, "请填写数字"],
            letters: [/^[a-z]+$/i, "请填写字母"],
            date: [/^\d{4}-\d{2}-\d{2}$/, "请填写有效的日期，格式:yyyy-mm-dd"],
            time: [/^([01]\d|2[0-3])(:[0-5]\d){1,2}$/, "请填写有效的时间，00:00到23:59之间"],
            email: [/^[\w\+\-]+(\.[\w\+\-]+)*@[a-z\d\-]+(\.[a-z\d\-]+)*\.([a-z]{2,4})$/i, "请填写有效的邮箱"],
            url: [/^(https?|s?ftp):\/\/\S+$/i, "请填写有效的网址"],
            qq: [/^[1-9]\d{4,}$/, "请填写有效的QQ号"],
            IDcard: [/^\d{6}(19|2\d)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)?$/, "请填写正确的身份证号码"],
            tel: [/^(?:(?:0\d{2,3}[\- ]?[1-9]\d{6,7})|(?:[48]00[\- ]?[1-9]\d{6}))$/, "请填写有效的电话号码"],
            mobile: [/^1[3-9]\d{9}$/, "请填写有效的手机号"],
            zipcode: [/^\d{6}$/, "请检查邮政编码格式"],
            chinese: [/^[\u0391-\uFFE5]+$/, "请填写中文字符"],
            username: [/^\w{3,12}$/, "请填写3-12位数字、字母、下划线"],
            password: [/^[\S]{6,16}$/, "请填写6-16位字符，不能包含空格"],
            accept: function(element, params) {
                if (!params) return true;
                let ext = params[0],
                    value = $(element).val();
                return (ext === "*") ||
                    (new RegExp(".(?:" + ext + ")$", "i")).test(value) ||
                    this.renderMsg("只接受{1}后缀的文件", ext.replace(/\|/g, ","));
            },
            // TODO 自定义规则
            isValidCronExpression: function(element) {
                return $.ajax({
                    url: getAgentName() + "/QuartzJob/isValidCronExpression.action",
                    type: "post",
                    data: element.name + "=" + element.value,
                    dataType: "json",
                });
            },
            isJson: function(element) {
                let str = element.value;
                if (typeof str == "string") {
                    try {
                        let obj = JSON.parse(str);
                        if (typeof obj == "object" && obj) {
                            return true;
                        } else {
                            return false;
                        }
                    } catch (e) {
                        return false;
                    }
                }
            },
            // 身份证
            IdCardNo: function(element) {
                let value = element.value,
                    isValid = true;
                let cityCode = {
                    11: "北京",
                    12: "天津",
                    13: "河北",
                    14: "山西",
                    15: "内蒙古",
                    21: "辽宁",
                    22: "吉林",
                    23: "黑龙江",
                    31: "上海",
                    32: "江苏",
                    33: "浙江",
                    34: "安徽",
                    35: "福建",
                    36: "江西",
                    37: "山东",
                    41: "河南",
                    42: "湖北",
                    43: "湖南",
                    44: "广东",
                    45: "广西",
                    46: "海南",
                    50: "重庆",
                    51: "四川",
                    52: "贵州",
                    53: "云南",
                    54: "西藏",
                    61: "陕西",
                    62: "甘肃",
                    63: "青海",
                    64: "宁夏",
                    65: "新疆",
                    71: "台湾",
                    81: "香港",
                    82: "澳门",
                    91: "国外",
                };

                /* 15位校验规则： (dddddd yymmdd xx g)    g奇数为男，偶数为女
                 * 18位校验规则： (dddddd yyyymmdd xxx p) xxx奇数为男，偶数为女，p校验位

                    校验位公式：C17 = C[ MOD( ∑(Ci*Wi), 11) ]
                        i----表示号码字符从由至左包括校验码在内的位置序号
                        Wi 7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 1
                        Ci 1 0 X 9 8 7 6 5 4 3 2
                 */
                let rFormat =
                    /^\d{6}(19|20)\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)$|^\d{6}\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}$/; // 格式验证

                if (!rFormat.test(value) || !cityCode[value.substr(0, 2)]) {
                    isValid = false;
                }
                // 18位身份证需要验证最后一位校验位
                else if (value.length === 18) {
                    let Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]; // 加权因子
                    let Ci = "10X98765432"; // 校验字符
                    // 加权求和
                    let sum = 0;
                    for (let i = 0; i < 17; i++) {
                        sum += value.charAt(i) * Wi[i];
                    }
                    // 计算校验值
                    let C17 = Ci.charAt(sum % 11);
                    // 与校验位比对
                    if (C17 !== value.charAt(17)) {
                        isValid = false;
                    }
                }
                return isValid || "请填写正确的身份证号码";
            },
            // 统一社会信用代码
            UnifiedSocialCreditCode: function(element) {
                let value = element.value.replace(/^\s*|\s*$/g, ""),
                    isValid = true,
                    rFormat = /^[1-9A-GV][1239][1-9]\d{5}[A-Z\d]{10}/; //[X\d][Y\d]

                if (!rFormat.test(value)) {
                    isValid = false;
                } else {
                    let code, Wi, Ci, sum, C18;
                    // 计算最后校验位：C18 = 31 - MOD ( ∑(Ci*Wi), 31 )
                    code = value.slice(0, 17);
                    Wi = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28];
                    Ci = "0123456789ABCDEFGHJKLMNPQRTUWXY";
                    // 加权求和
                    sum = 0;
                    for (let i = 0; i < Wi.length; i++) {
                        sum += Ci.indexOf(code.charAt(i)) * Wi[i];
                    }
                    C18 = 31 - (sum % 31);
                    // 与校验位比对
                    if (value.charAt(17) !== Ci.charAt(C18)) {
                        isValid = false;
                    }
                }

                return isValid || "请填写正确的统一社会信用代码";
            },
            //营业执照代码
            BusinessLicenseCode: function(element) {
                let code = element.value.replace(/^\s*|\s*$/g, ""),
                    isValid = true;

                if (code.length != 15) {
                    isValid = false;
                } else {
                    let aj, sj, pj;
                    aj = 0, sj = 0, pj = 10;
                    for (let j = 1; j < 15; j++) {
                        //aj 第j位数字,标识a15-j+1 (下标15-j+1)
                        aj = Number(code.charAt(j - 1));
                        // sj 第j位 计算值
                        sj = pj % 11 + aj;
                        // p(j+1) 第j位 计算值(用于下一位计算)
                        pj = (0 == sj % 10 ? 10 : sj % 10) * 2;
                    }
                    // 第15位
                    aj = 11 - pj % 11, aj = 10 == aj ? 0 : aj;
                    // 与校验位比对
                    isValid = aj == code.charAt(14);
                }
                return isValid || "请填写正确的营业执照代码";
            },
            //组织机构代码
            OrgCode: function(element) {
                let code = element.value,
                    isValid = true;
                if (code.length != 9) {
                    isValid = false;
                } else {
                    code = code.substr(0, 8) + "-" + code.substr(8, 1);
                    let ws = [3, 7, 9, 10, 5, 8, 4, 2];
                    let str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                    let reg = /^([0-9A-Z]){8}-[0-9|X]$/; // /^[A-Za-z0-9]{8}-[A-Za-z0-9]{1}$/  
                    let sum = 0;
                    for (let i = 0; i < 8; i++) {
                        sum += str.indexOf(code.charAt(i)) * ws[i];
                    }
                    let c9 = 11 - (sum % 11);
                    c9 = c9 == 10 ? "X" : c9;
                    if (!reg.test(code) || c9 == code.charAt(9)) {
                        isValid = true;
                    } else {
                        isValid = false;
                    }
                }
                return isValid || "请填写正确的组织机构代码";
            },
            baseCheck_nullRule: function(element, params, field) {
                return this.test(element, "required") === false ? undefined : "必空";
            },
            baseCheck_notNullRule: function(element, params, field) {
                return this.test(element, "required") === true ? undefined : "必填";
            },
            baseCheck_optionalRule: function(element, params, field) { // 选填
                setTimeout(function() {
                    $(element).trigger("showmsg", ["tip", "选填"]);
                }, 1000);
                return undefined;
            },
            baseCheck_dateRule: function(element, params, field) {
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let format = unescape(params[0]);
                    return Date.isValiDate(element.value, format) ? undefined : "请填写正确的日期";
                } else {
                    return undefined;
                }
            },
            baseCheck_dictRule: function(element, params, field) {
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param, paramArr, dictNo, fDictNo, fOptCode, delimiter, optName, isValid;
                    param = unescape(params[0]), paramArr = param.split(","), dictNo = paramArr[0];
                    if (paramArr.length === 3) {
                        fDictNo = paramArr[1], fOptCode = element.form[paramArr[2]].value;
                    }
                    delimiter = element.getAttribute("delimiter");
                    if (delimiter) {
                        optName = getOptNameNew(dictNo, element.value, true, delimiter, fDictNo, fOptCode);
                    } else {
                        optName = getOptNameNew(dictNo, element.value, undefined, undefined, fDictNo, fOptCode);
                    }
                    isValid = (optName !== undefined && optName !== "");

                    return isValid ? undefined : "空值或不在数据字典项中";
                } else {
                    return undefined;
                }
            },
            baseCheck_equalRule: function(element, params, field) { //等于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_equalRule异常：缺失参数");
                        sAlert("基础校验-【等于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            return this.test(element, "match(eq," + key + ")") === true ? undefined : ("必须等于" + label);
                        } else {
                            if (/select/.test(element.type)) {
                                let text = element.options[element.selectedIndex].text;
                                return element.value == param === true ? undefined : ("必须选择：" + text);
                            } else {
                                return element.value == param === true ? undefined : ("必须等于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_notEqualRule: function(element, params, field) { //不等于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_notEqualRule异常：缺失参数");
                        sAlert("基础校验-【不等于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            return this.test(element, "match(neq," + key + ")") === true ? undefined : ("必须不等于" + label);
                        } else {
                            if (/select/.test(element.type)) {
                                let text = element.options[element.selectedIndex].text;
                                return element.value != param === true ? undefined : ("不可选择：" + text);
                            } else {
                                return element.value != param === true ? undefined : ("必须不等于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_greaterEqualRule: function(element, params, field) { //大于等于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_greaterEqualRule异常：缺失参数");
                        sAlert("基础校验-【大于等于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            if (element.getAttribute("datatype") == "date") { // 日期类
                                return this.test(element, "match(gte, " + key + ", date)") === true ? undefined : ("必须大于等于" + label);
                            } else {
                                return this.test(element, "match(gte, " + key + ")") === true ? undefined : ("必须大于等于" + label);
                            }
                        } else {
                            if (element.getAttribute("datatype") == "date") {
                                return new Date(element.value) >= new Date(param) ? undefined : ("必须大于等于" + param);
                            } else {
                                return this.test(element, "range(" + param + "~)") === true ? undefined : ("必须大于等于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_lessEqualRule: function(element, params, field) { //小于等于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_lessEqualRule异常：缺失参数");
                        sAlert("基础校验-【小于等于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            if (element.getAttribute("datatype") == "date") { // 日期类
                                return this.test(element, "match(lte, " + key + ", date)") === true ? undefined : ("必须小于等于" + label);
                            } else {
                                return this.test(element, "match(lte, " + key + ")") === true ? undefined : ("必须小于等于" + label);
                            }
                        } else {
                            if (element.getAttribute("datatype") == "date") { //日期类
                                return new Date(element.value) <= new Date(param) ? undefined : ("必须小于等于" + param);
                            } else {
                                return this.test(element, "range(~" + param + ")") === true ? undefined : ("必须小于等于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_greaterRule: function(element, params, field) { //大于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_greaterRule异常：缺失参数");
                        sAlert("基础校验-【大于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            if (element.getAttribute("datatype") == "date") { // 日期类
                                return this.test(element, "match(gt, " + key + ", date)") === true ? undefined : ("必须大于" + label);
                            } else {
                                return this.test(element, "match(gt, " + key + ")") === true ? undefined : ("必须大于" + label);
                            }
                        } else {
                            if (element.getAttribute("datatype") == "date") {
                                return new Date(element.value) > new Date(param) ? undefined : ("必须大于" + param);
                            } else {
                                return this.test(element, "range(" + param + "~, false)") === true ? undefined : ("必须大于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_lessRule: function(element, params, field) { //小于
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_lessRule异常：缺失参数");
                        sAlert("基础校验-【小于】规则缺失参数", "异常");
                        return false;
                    }
                    if (element.value) {
                        if (/^\${.*}$/.test(param)) { // 变量
                            let key = param.match(/(?<=\${)(.*)(?=})/);
                            let label = element.form[key].getAttribute("label");
                            if (element.getAttribute("datatype") == "date") { // 日期类
                                return this.test(element, "match(lt, " + key + ", date)") === true ? undefined : ("必须小于" + label);
                            } else {
                                return this.test(element, "match(lt, " + key + ")") === true ? undefined : ("必须小于" + label);
                            }
                        } else {
                            if (element.getAttribute("datatype") == "date") { //日期类
                                return new Date(element.value) < new Date(param) ? undefined : ("必须小于" + param);
                            } else {
                                return this.test(element, "range(~" + param + ", false)") === true ? undefined : ("必须小于" + param);
                            }
                        }
                    }
                } else {
                    return undefined;
                }
            },
            baseCheck_fixedLengthRule: function(element, params, field) { //固定长度
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_fixedLengthRule：缺失参数");
                        sAlert("固定长度基础校验：缺失参数", "异常");
                        return false;
                    }
                    param = param.trim();

                    let reg = /^([1-9]+\d*)(?:\s*?,\s*?)?(0|1)?(?:\s*?,\s*?)?(UTF-8|GB18030)?$/;
                    if (reg.test(param)) {
                        let requiredLength, type, charset, v, length;
                        let rs = param.match(reg);
                        requiredLength = rs[1], type = rs[2] || "0", charset = rs[3] || "UTF-8";
                        // console.log(requiredLength, type, charset)
                        v = element.value, length = v.length;
                        if (type == "1") { //字符
                            // 字符就是它的长度,不需要额外处理
                        } else { //字节
                            if (/[^\x00-\xff]/.test(v)) { // 是否包含非键盘字符
                                let _length = v.match(/[^\x00-\xff]/g).length; //非键盘字符个数
                                if (charset == "GB18030") { // 双字节(GB18030)
                                    //console.log('双字节(GB18030)');
                                    length += _length; // 在原有基础上加上
                                } else { // 中文(UTF-8)
                                    //console.log('中文(UTF-8)(默认)');
                                    length += _length * 2; // 在原有基础上加上
                                }
                            }
                        }
                        //var label = element.getAttribute('label');
                        return requiredLength == length ? undefined : ("固定长度" + requiredLength + "位");
                    } else {
                        sAlert("固定长度基础校验：不合法的参数", "异常");
                        return false;
                    }
                } else {
                    return undefined; // 空则返回undefined,跳过本条规则
                }
            },
            baseCheck_maxLengthRule: function(element, params, field) { //最大长度
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_maxLengthRule：缺失参数");
                        sAlert("最大长度基础校验：缺失参数", "异常");
                        return false;
                    }
                    param = param.trim();

                    let reg = /^([1-9]+\d*)(?:\s*?,\s*?)?(0|1)?(?:\s*?,\s*?)?(UTF-8|GB18030)?$/;
                    if (reg.test(param)) {
                        let requiredLength, type, charset, v, length;
                        let rs = param.match(reg);
                        requiredLength = rs[1], type = rs[2] || "0", charset = rs[3] || "UTF-8";
                        //console.log(requiredLength, type, charset)
                        v = element.value, length = v.length;
                        if (type == "1") { //字符
                            // 字符就是它的长度,不需要额外处理
                        } else { //字节
                            if (/[^\x00-\xff]/.test(v)) { // 是否包含非键盘字符
                                let _length = v.match(/[^\x00-\xff]/g).length; //非键盘字符个数
                                if (charset == "GB18030") { // 双字节(GB18030)
                                    //console.log('双字节(GB18030)');
                                    length += _length; // 在原有基础上加上
                                } else { // 中文(UTF-8)
                                    //console.log('中文(UTF-8)(默认)');
                                    length += _length * 2; // 在原有基础上加上
                                }
                            }
                        }
                        //var label = element.getAttribute('label');
                        return requiredLength >= length ? undefined : ("最大长度" + requiredLength + "位");
                    } else {
                        sAlert("最大长度基础校验：不合法的参数", "异常");
                        return false;
                    }
                } else {
                    return undefined; // 空则返回undefined,跳过本条规则
                }
            },
            baseCheck_minLengthRule: function(element, params, field) { //最小长度
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_minLengthRule：缺失参数");
                        sAlert("最小长度基础校验：缺失参数", "异常");
                        return false;
                    }
                    param = param.trim();

                    let reg = /^([1-9]+\d*)(?:\s*?,\s*?)?(0|1)?(?:\s*?,\s*?)?(UTF-8|GB18030)?$/;
                    if (reg.test(param)) {
                        let requiredLength, type, charset, v, length;
                        let rs = param.match(reg);
                        requiredLength = rs[1], type = rs[2] || "0", charset = rs[3] || "UTF-8";
                        // console.log(requiredLength, type, charset)
                        v = element.value, length = v.length;
                        if (type == "1") { //字符
                            // 字符就是它的长度,不需要额外处理
                        } else { //字节
                            if (/[^\x00-\xff]/.test(v)) { // 是否包含非键盘字符
                                let _length = v.match(/[^\x00-\xff]/g).length; //非键盘字符个数
                                if (charset == "GB18030") { // 双字节(GB18030)
                                    //console.log('双字节(GB18030)');
                                    length += _length; // 在原有基础上加上
                                } else { // 中文(UTF-8)
                                    //console.log('中文(UTF-8)(默认)');
                                    length += _length * 2; // 在原有基础上加上
                                }
                            }
                        }
                        //var label = element.getAttribute('label');
                        return requiredLength <= length ? undefined : ("最小长度" + requiredLength + "位");
                    } else {
                        sAlert("最小长度基础校验：不合法的参数", "异常");
                        return false;
                    }
                } else {
                    return undefined; // 空则返回undefined,跳过本条规则
                }
            },
            baseCheck_regExpRule: function(element, params, field) { //最小长度
                /*
                 * 只校验非空的
                 */
                if (element.value) {
                    let param = unescape(params[0]);
                    let desc = unescape(params[1]);
                    if (param == undefined || param == "") {
                        console.error("baseCheck_minLengthRule：缺失参数");
                        sAlert("最小长度基础校验：缺失参数", "异常");
                        return false;
                    }
                    param = param.trim();
                    // 判断 正则 三元
                    return new RegExp(param).test(element.value) ? undefined : ("不满足正则格式：" + param + "，" + desc);
                } else {
                    return undefined; // 空则返回undefined,跳过本条规则
                }
            },
            logicCheck_baseCheck: function(element, params, field) {
                let preCondition = unescape(params[0]);
                let checkRule = unescape(params[1]);
                let ruleDesc = unescape(params[2]);
                let currentColumnName = element.name; //当前input name
                //console.log("logicCheck_baseCheck", currentColumnName, preCondition, checkRule, ruleDesc)

                // 前置条件判断
                let preChcekResult = logicCheck_preCheck(element, params, field);
                let preColumnName = preChcekResult.columnName;
                let preIsValid = preChcekResult.isValid;
                //console.log("preColumnName", preColumnName);
                if (preIsValid) {
                    let ruleChcekResult = logicCheck_ruleCheck(element, params, field);
                    return ruleChcekResult.isValid ? undefined : ruleDesc;
                } else {
                    // 前置条件不通过,undefined-不影响验证结果不提示消息（继续验证下一个规则）
                    return undefined;
                }
            },
            logicCheck_linkage: function(element, params, field) {
                let preCondition = unescape(params[0]);
                let checkRule = unescape(params[1]);
                let ruleDesc = unescape(params[2]);
                let currentColumnName = element.name; //当前input name
                //console.log("logicCheck_linkage", currentColumnName, preCondition, checkRule, ruleDesc)

                // 前置条件判断
                let preChcekResult = logicCheck_preCheck(element, params, field);
                let preColumnName = preChcekResult.columnName;
                let preIsValid = preChcekResult.isValid;
                //console.log("preColumnName", preColumnName, "preIsValid", preIsValid);
                if (preIsValid) {
                    try {
                        logicCheck_linkage(element, params, field);
                    } catch (e) {
                        console.error("logicCheck_linkage异常", preCondition, checkRule, e);
                        sAlert("逻辑校验-联动<br>" + checkRule + "<br>请联系管理员！", "异常");
                    }
                }
                // 联动始终返回undefined-不影响验证结果不提示消息（继续验证下一个规则）
                return undefined;
            },
            logicCheck_DBBJ: function(element, params, field) {
                //console.log("logicCheck_isNull");
                let preCondition = unescape(params[0]);
                let checkRule = unescape(params[1]);
                let ruleDesc = unescape(params[2]);
                let currentColumnName = element.name; //当前input name
                //console.log("preCondition", preCondition);
                //console.log("checkRule", checkRule);

                // 前置条件判断
                let preChcekResult = logicCheck_preCheck(element, params, field);
                let preColumnName = preChcekResult.columnName;
                let preIsValid = preChcekResult.isValid;
                if (preIsValid) {
                    // 前置条件通过
                    if (currentColumnName === preColumnName) { // 当前字段是前置字段-联动
                        console.log("未发现匹配的处理规则,请书写对应JavaScript代码");
                        return "未发现匹配的处理规则,请书写对应JavaScript代码";
                    } else { //当前字段为校验字段-校验
                        let reg = new RegExp("DBBJ\\(|'|\\)", "g");
                        let checkRuleArr = checkRule.replace(reg, "").split(",");
                        let value = element.form[checkRuleArr[0]].value || "0";
                        let type = checkRuleArr[1];
                        value = Number(value.replace(new RegExp(",", "g"), ""));
                        if (NaN === value) {
                            return ruleDesc;
                        }
                        if (type === "0") { //空或
                            return value == 0 ? undefined : ruleDesc;
                        } else if (type === "1") {
                            return value > 0 ? undefined : ruleDesc;
                        } else {
                            return ruleDesc;
                        }
                    }
                } else {
                    // 前置条件不通过,undefined-不影响验证结果不提示消息（继续验证下一个规则）
                    return undefined;
                }
            },
            logicCheck_isFinLicCode: function(element, params, field) {
                let preCondition = unescape(params[0]);
                let checkRule = unescape(params[1]);
                let ruleDesc = unescape(params[2]);
                let currentColumnName = element.name; //当前input name

                // 前置条件判断
                let preChcekResult = logicCheck_preCheck(element, params, field);
                let preColumnName = preChcekResult.columnName;
                let preIsValid = preChcekResult.isValid;

                if (preIsValid) {
                    // 前置条件通过
                    if (currentColumnName === preColumnName) { // 当前字段是前置字段
                        console.log("未发现匹配的处理规则,请书写对应JavaScript代码");
                        return "未发现匹配的处理规则,请书写对应JavaScript代码";
                    } else { //当前字段为校验字段
                        let reg_replace = new RegExp("isFinLicCode\\(|\\)", "g");
                        let columnName = checkRule.replace(reg_replace, "");
                        let value = element.form[columnName].value;
                        let reg = new RegExp("(A|B|C|D|E|F|J|K|N|L|M|P|Q|Z)[0-9]{4}.{10}");
                        return reg.test(value) ? undefined : ruleDesc;
                    }
                } else {
                    // 前置条件不通过,undefined-不影响验证结果不提示消息（继续验证下一个规则）
                    return undefined;
                }
            },

        },

        // Default error messages
        messages: {
            0: "此处",
            fallback: "{0}格式不正确",
            loading: "正在验证...",
            error: "网络异常",
            timeout: "请求超时",
            required: "{0}不能为空",
            remote: "{0}已被使用",
            integer: {
                "*": "请填写整数",
                "+": "请填写正整数",
                "+0": "请填写正整数或0",
                "-": "请填写负整数",
                "-0": "请填写负整数或0",
            },
            match: {
                eq: "{0}与{1}不一致",
                neq: "{0}与{1}不能相同",
                lt: "{0}必须小于{1}",
                gt: "{0}必须大于{1}",
                lte: "{0}不能大于{1}",
                gte: "{0}不能小于{1}",
            },
            range: {
                rg: "请填写{1}到{2}的数",
                gte: "请填写不小于{1}的数",
                lte: "请填写最大{1}的数",
                gtlt: "请填写{1}到{2}之间的数",
                gt: "请填写大于{1}的数",
                lt: "请填写小于{1}的数",
            },
            checked: {
                eq: "请选择{1}项",
                rg: "请选择{1}到{2}项",
                gte: "请至少选择{1}项",
                lte: "请最多选择{1}项",
            },
            length: {
                eq: "请填写{1}个字符",
                rg: "请填写{1}到{2}个字符",
                gte: "请至少填写{1}个字符",
                lte: "请最多填写{1}个字符",
                eq_2: "",
                rg_2: "",
                gte_2: "",
                lte_2: "",
            },
            // TODO 自定义规则提示信息
            isJson: "请填写Json字符串",
            logicCheck_xtdjxtcpbh: "11111",
        },
    });

    function logicCheck_baseCheck(element, params, field, condition) {
        /*
         * 原理 通过正则匹配表达式,然后处理,再使用返回的true或false替换表达式,最终eval得出最终校验结果
         * 若无法匹配,这无法替换,将直接报错提醒
         */
        //console.log('logicCheck_baseCheck');
        //console.log(condition);

        let columnName, isValid = false,
            regexpString = "";

        //字段比较(包含加减乘除,但不支持括号运算)
        regexpString += "([a-zA-Z0-9_]+(!=|>|>=|==|<=|<)([^!|&&|\\|\\||\\(|\\)]+))";

        /*******方法******/
        //转为date
        regexpString += "|date\\(.*?\\)";
        //length
        regexpString += "|length\\(.*?\\)";
        //true
        regexpString += "|optional\\(.*?\\)";
        /*******校验器**********/
        //是空
        regexpString += "|isNull\\(.*?\\)";
        //非空
        regexpString += "|isNotNull\\(.*?\\)";
        //在
        regexpString += "|isIn\\(.*?(,'.*?')+\\)";
        //不在
        regexpString += "|isNotIn\\(.*?(,'.*?')+\\)";
        //是字典项
        regexpString += "|isDictItem\\(.*?\\)";
        //身份证
        regexpString += "|isIdCardNo\\(.*?\\)";
        //统一社会信用代码
        regexpString += "|isCreditCode\\(.*?\\)";
        //营业执照代码
        regexpString += "|isBusinessLicenseCode\\(.*?\\)";
        //组织机构代码
        regexpString += "|isOrgCode\\(.*?\\)";
        //行政区划代码
        regexpString += "|isAreaCode\\(.*?\\)";
        //邮编
        regexpString += "|isPostCode\\(.*?\\)";
        //金融许可证
        regexpString += "|isFinLicCode\\(.*?\\)";
        //文本包含
        regexpString += "|string\\.contains\\(.*?,'.*?'\\)";
        //数组包含
        regexpString += "|include\\(string\\.split\\(.*?,'(?:,|;|,\\|;)'\\),'.*?'\\)";
        //以某些字符串开头
        regexpString += "|startWith\\(.*?(,'.*?')+\\)";
        //以某些字符串开头
        regexpString += "|endWith\\(.*?(,'.*?')+\\)";
        //转为double
        regexpString += "|doubleValue\\(.*?\\)";
        //舍入
        //regexpString += "|round\\(.*?\\)"; //舍入的应该都是联动，而没有前置校验的，先不处理
        //正则表达式
        regexpString += "|regExp\\(.*?\\)(?=(?:[^']*(?:'[^']*')?[^']*)*$)"; // 排除引号中正则表达式的括号

        let macthResult = condition.match(new RegExp(regexpString, "g"));
        //console.log("condition", condition, macthResult);
        if (null == macthResult) {
            console.log("未发现匹配的处理规则,请书写对应JavaScript代码", condition);
            sAlert("未发现匹配的处理规则,请书写对应JavaScript代码<br>" + condition, "异常");
            return {
                columnName: "",
                isValid: isValid,
            };
        } else {
            for (let i = 0, len = macthResult.length; i < len; i++) {
                let result, _condition = macthResult[i];
                // 普通方法
                if (_condition.indexOf("length") != -1) {
                    result = f_length(element, params, field, _condition);
                } else if (_condition.indexOf("doubleValue") != -1) {
                    result = f_doubleValue(element, params, field, _condition);
                } else if (_condition.indexOf("date") != -1) {
                    result = f_date(element, params, field, _condition);
                }
                // 校验器
                else if (_condition.indexOf("optional") != -1) {
                    result = v_optional(element, params, field, _condition);
                } else if (_condition.indexOf("isNotNull") != -1) {
                    result = v_isNotNull(element, params, field, _condition);
                } else if (_condition.indexOf("isNull") != -1) {
                    result = v_isNull(element, params, field, _condition);
                } else if (_condition.indexOf("isNotIn") != -1) {
                    result = v_isNotIn(element, params, field, _condition);
                } else if (_condition.indexOf("isIn") != -1) {
                    result = v_isIn(element, params, field, _condition);
                } else if (_condition.indexOf("isDictItem") != -1) {
                    result = v_isDictItem(element, params, field, _condition);
                } else if (_condition.indexOf("isIdCardNo") != -1) {
                    result = v_isIdCardNo(element, params, field, _condition);
                } else if (_condition.indexOf("isCreditCode") != -1) {
                    result = v_isCreditCode(element, params, field, _condition);
                } else if (_condition.indexOf("isBusinessLicenseCode") != -1) {
                    result = v_isBusinessLicenseCode(element, params, field, _condition);
                } else if (_condition.indexOf("isAreaCode") != -1) {
                    result = v_isAreaCode(element, params, field, _condition);
                } else if (_condition.indexOf("isPostCode") != -1) {
                    result = v_isPostCode(element, params, field, _condition);
                } else if (_condition.indexOf("isFinLicCode") != -1) {
                    result = v_isFinLicCode(element, params, field, _condition);
                } else if (_condition.indexOf("isOrgCode") != -1) {
                    result = v_isOrgCode(element, params, field, _condition);
                } else if (_condition.indexOf("string.contains") != -1) {
                    result = v_contains(element, params, field, _condition);
                } else if (_condition.indexOf("include") != -1) {
                    result = v_include(element, params, field, _condition);
                } else if (_condition.indexOf("startWith") != -1) {
                    result = v_startWith(element, params, field, _condition);
                } else if (_condition.indexOf("endWith") != -1) {
                    result = v_endWith(element, params, field, _condition);
                } else if (_condition.indexOf("regExp") != -1) {
                    result = v_regExp(element, params, field, _condition);
                } else {
                    result = v_basicOperations(element, params, field, _condition);
                }
                columnName = result.columnName, isValid = result.isValid;
                condition = condition.replace(_condition, isValid);
            }
            //console.log("columnName", columnName, "replaceCondition", condition);
            //逻辑符号与或非替换为math识别的 注:math默认的!=不能替换!为not,否者报错,类似!(1==2)的可以替换
            isValid = math.evaluate(condition.replace(/&&/g, " and ").replace(/\|\|/g, " or ").replace(/!(?!=)/g, " not "));
            //console.log("isValid", isValid);
            return {
                columnName: columnName,
                isValid: isValid,
            };
        }
    }

    /**
     * 对包含小数的字符串进行处理(升幂降幂),避免精度丢失
     * @param {String} condition
     * @deprecated 使用math代替
     */
    function getNewConditionOfDecimal(condition) {
        // 169248000.00==1376000000.00*12.300/100
        let decimalArr = condition.match(/\d+(\.\d*)?/g); //获取所有数值
        let sortArr = decimalArr.concat();
        sortArr.sort(function sortNumber(a, b) { //a.length == b.length ? b - a : b.length - a.length; 
            return b.length - a.length; // 排序,先长后短,后续正则优先匹配长的,否则split将会异常
        });
        let operatorArr = condition.split(new RegExp(sortArr.join("|"), "g")); //获取所有非数值,可能会有空字符串出现,需要处理
        let scaleArr = []; // 存储每个浮点数小数点后位数,用于获取最大值
        for (let i = 0, len = decimalArr.length; i < len; i++) {
            if (/^\d+\.\d+$/.test(decimalArr[i])) { //小数,否者split报错
                scaleArr.push(("" + decimalArr[i]).split(".")[1].length);
            }
        }
        let m = Math.pow(10, Math.max.apply(null, scaleArr)) || 1; //获取最大小数点位数
        let newArr = operatorArr.concat(); // 新数组
        for (let i = 0, len = decimalArr.length; i < len; i++) {
            if (/==/.test(newArr[2 * i])) {
                newArr[2 * i] = newArr[2 * i].replace("==", "/" + m + "==("); // 左侧降幂,同时包裹右侧(左括号)
            }
            newArr.splice(2 * i + 1, 0, "(" + decimalArr[i] + "*" + m + ")"); //升幂并合并
        }
        if (!/==/.test(condition)) {
            newArr.unshift("("); //包裹,左括号
        }
        newArr.push(")/" + m); // 右侧包裹(右括号),并降幂
        condition = newArr.join(""); // 新的condition
        return condition;
    }

    /**************方法***************/
    // 获取长度
    function f_length(element, params, field, condition) {
        //length(wtrzjhm)
        let columnName, length;
        columnName = condition.replace(new RegExp("length\\(|\\)", "g"), "");
        length = element.form[columnName].value.length;
        return {
            columnName: columnName,
            isValid: length,
        };
    }
    // 获取double值
    function f_doubleValue(element, params, field, condition) {
        //doubleValue(zggdgmzfw) 
        //console.log('f_doubleValue', condition);
        let columnName, value, numberType;
        columnName = condition.replace(new RegExp("doubleValue\\(|\\)", "g"), "");
        value = element.form[columnName].value.replace(/,/g, "") || 0;

        numberType = element.form[columnName].getAttribute("numberType");

        if ("P" == numberType) { //以百分比展示的字段,乘以了100,计算时需要除以100
            value = value / 100;
        }

        return {
            columnName: columnName,
            isValid: value,
        };
    }
    /**
     * 转为date值
     * 样例：date(cpjhdqr,'yyyy-MM-dd') date('9999-12-31,'yyyy-MM-dd')
     */
    function f_date(element, params, field, condition) {
        //console.log("f_date", element.name, condition);
        let arr, pattern, columnName, value;
        arr = condition.match(/(?<=\()([^']+?)(?=,)|(?<=\('|,')([^']+?)(?=')/g), columnName = arr[0], pattern = arr[1];
        if (element.form[columnName]) { //date(cpjhdqr,'yyyy-MM-dd')
            value = Date.parseDate(element.form[columnName].value, pattern);
            value = value ? value.getTime() : element.form[columnName].value || 0;
        } else { // date('9999-12-31,'yyyy-MM-dd')
            value = Date.parseDate(columnName, pattern).getTime();
        }
        return {
            columnName: columnName,
            isValid: value,
        };
    }

    /***********校验器************/
    // 选填
    function v_optional(element, params, field, condition) {
        //optional(qtbgywlx)
        let columnName, value, isValid;
        columnName = condition.match(/optional\((.+?)\)/)[1];
        value = element.form[columnName].value, isValid = true;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isNotNull(element, params, field, condition) {
        //isNotNull(qtbgywlx)   isNotNull('ge',1,syryqsylqj_zd,syryqsylqj_zg)
        let preCondition = unescape(params[0]);
        let rule = unescape(params[1]);
        let ruleDesc = unescape(params[2]);
        //console.log("v_isNotNull", element.name, preCondition, rule, ruleDesc)
        let columnName, value, isValid, relationalOperator, require, count;
        let paramArr = condition.match(/isNotNull\((.+?)\)/)[1].split(",");
        if (paramArr.length === 1) {
            columnName = paramArr[0];
            value = element.form[columnName].value, isValid = undefined !== value && value !== "";
        } else {
            //提示绑定字段用第一个字段
            columnName = paramArr[2], relationalOperator = paramArr[0].replace(/'/g, "");
            require = paramArr[1], count = 0;
            for (let i = 2, len = paramArr.length; i < len; i++) {
                let colName = paramArr[i];
                value = element.form[colName].value, isValid = undefined !== value && value !== "";
                if (isValid) count++;
            }
            if ("eq" == relationalOperator) {
                isValid = count == require;
            } else if ("ge" == relationalOperator) {
                isValid = count >= require;
            } else {
                isValid = false;
                throw "参数异常：" + relationalOperator;
            }

            // 1.触发字段必须为同类字段才校验同类数据，否者内外元素对象非同类，data赋值清除存在问题，容易引起死循环
            // 2.为简化直接使用 绑定字段，同时降低重复循环次数
            if (element.name == columnName && !$(element.form[columnName]).data("_validated_")) {
                for (let i = 2, len = paramArr.length; i < len; i++) {
                    let colName = paramArr[i];
                    $(element.form[colName]).data("_validated_", 1);
                }
                for (let i = 2, len = paramArr.length; i < len; i++) {
                    let colName = paramArr[i];
                    if (element !== element.form[colName]) {
                        $(element.form[colName]).isValid();
                    }
                }
                for (let i = 2, len = paramArr.length; i < len; i++) {
                    let colName = paramArr[i];
                    $(element.form[colName]).removeData("_validated_");
                }
            }
        }

        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isNull(element, params, field, condition) {
        //isNotNull(qtbgywlx)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isNull\\(|\\)|'", "g"), "");
        value = element.form[columnName].value, isValid = undefined === value || value === "";
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isNotIn(element, params, field, condition) {
        //isNotIn(qtbgywlx)
        let arr, columnName, inArr, value, isValid;
        arr = condition.replace(new RegExp("isNotIn\\(|\\)|'", "g"), "").split(","), columnName = arr[0], inArr = arr.slice(1);
        value = element.form[columnName].value, isValid = inArr.indexOf(value) == -1;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isIn(element, params, field, condition) {
        //isIn(syrsyllx,'0','1')
        let arr, columnName, inArr, value, isValid;
        arr = condition.replace(new RegExp("isIn\\(|\\)|'", "g"), "").replace(new RegExp("kong", "g"), "").split(",");
        columnName = arr[0], inArr = arr.slice(1);
        value = element.form[columnName].value, isValid = inArr.indexOf(value) != -1;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isDictItem(element, params, field, condition) {
        //isDictItem(lxxq_wtr,'ZXD_WTRSYRLXXQ')  普通字段,2个参数
        //isDictItem(wtrzjlx,'ZXD_WTRSYRZJLX','ZXD_WTRSYRLX',wtrlx) 联动字段,4个参数,带有上级字典项参数及字段
        let arr, columnName, dictNo, fDictNo, fOptCode, optName, value, isValid;
        arr = condition.replace(new RegExp("isDictItem\\(|\\)|'", "g"), "").split(","), columnName = arr[0], dictNo = arr[1];
        if (arr.length === 4) {
            fDictNo = arr[2], fOptCode = element.form[arr[3]].value;
        }
        value = element.form[columnName].value;
        optName = getOptNameNew(dictNo, value, undefined, undefined, fDictNo, fOptCode);
        isValid = (optName !== undefined && optName !== "");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    //身份证
    function v_isIdCardNo(element, params, field, condition) {
        //isIdCardNo(fddbrzjhm)
        let columnName, isValid;
        columnName = condition.replace(new RegExp("isIdCardNo\\(|\\)|'", "g"), "");
        isValid = field.validator.test(element.form[columnName], "IdCardNo");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    // 统一社会代码
    function v_isCreditCode(element, params, field, condition) {
        //isCreditCode(zjdm)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isCreditCode\\(|\\)|'", "g"), "");
        isValid = field.validator.test(element.form[columnName], "UnifiedSocialCreditCode");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    // 营业执照代码
    function v_isBusinessLicenseCode(element, params, field, condition) {
        //isBusinessLicenseCode(zjdm)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isBusinessLicenseCode\\(|\\)|'", "g"), "");
        isValid = field.validator.test(element.form[columnName], "BusinessLicenseCode");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isOrgCode(element, params, field, condition) {
        //isCreditCode(zjdm)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isOrgCode\\(|\\)|'", "g"), "");
        isValid = field.validator.test(element.form[columnName], "OrgCode");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isAreaCode(element, params, field, condition) {
        //isAreaCode(zcdq)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isAreaCode\\(|\\)|'", "g"), "");
        value = element.form[columnName].value, isValid = value.length === 6;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isPostCode(element, params, field, condition) {
        //isPostCode(yzbm)
        let columnName, isValid;
        columnName = condition.replace(new RegExp("isPostCode\\(|\\)|'", "g"), "");
        isValid = field.validator.test(element.form[columnName], "zipcode");
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_isFinLicCode(element, params, field, condition) {
        //isFinLicCode(gdzjhm)
        let columnName, value, isValid;
        columnName = condition.replace(new RegExp("isFinLicCode\\(|\\)|'", "g"), "");
        value = element.form[columnName].value, isValid = /(A|B|C|D|E|F|J|K|N|L|M|P|Q|Z)[0-9]{4}.{10}/.test(value);
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_contains(element, params, field, condition) {
        //string.contains(xmtjjg,'银行')  
        let arr, columnName, delimiter, containsValue, value;
        arr = condition.replace(new RegExp("string.contains\\(|\\)", "g"), "").split(",");
        columnName = arr[0], containsValue = arr[1].replace(/'/g, "");
        value = element.form[columnName].value, isValid = value.indexOf(containsValue) != -1;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_include(element, params, field, condition) {
        //include(string.split(bgywlx,','),'2')   bgywlx通常为String类型,会使用str(bgywlx)避免null值,结果将转为'null'字符串
        let arr, columnName, delimiter, includeValue, valueArr;
        arr = condition.replace(new RegExp("include\\(string.split\\(str\\(|\\)", "g"), "").split(/,(?=(?:[^']*(?:'[^']*')?[^']*)*$)/);
        columnName = arr[0], delimiter = arr[1].replace(/'/g, ""), includeValue = arr[2].replace(/'/g, "");
        // 20200622 delimiter通常有两种,所以直接改为(,|;)
        valueArr = element.form[columnName].value.split(/,|;/), isValid = valueArr.indexOf(includeValue) != -1;
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_startWith(element, params, field, condition) {
        //isNotIn(qtbgywlx)
        let arr, columnName, strArr, value, isValid;
        arr = condition.replace(new RegExp("startWith\\(|\\)|'", "g"), "").split(","), columnName = arr[0], strArr = arr.slice(1);
        value = element.form[columnName].value;

        for (i = 0, len = strArr.length; i < len; i++) {
            isValid = value.indexOf(strArr[i]) == 0;
            if (isValid) break;
        }

        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_endWith(element, params, field, condition) {
        //endWith(qtbgywlx,'9999')
        let arr, columnName, strArr, value, isValid;
        arr = condition.replace(new RegExp("endWith\\(|\\)|'", "g"), "").split(","), columnName = arr[0], strArr = arr.slice(1);
        value = element.form[columnName].value;

        for (i = 0, len = strArr.length; i < len; i++) {
            isValid = new RegExp(strArr[i] + "$").test(value);
            if (isValid) break;
        }

        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_regExp(element, params, field, condition) {
        //regExp(qtbgywlx,'正则表达式')
        let arr, columnName, regExpString, value, isValid;
        //arr = condition.replace(new RegExp("regExp\\(|\\)|'", "g"), "").split(/,(?=(\s*?)')/);
        //columnName = arr[0], regExpString = arr[1];
        columnName = condition.match(/(?<=regExp\(\s*)(\w+?)(?=\s*,)/)[0];
        regExpString = condition.match(/(?<=\s*')(.*)(?=\s*')/)[0];
        value = element.form[columnName].value;

        // 判断 正则 三元
        isValid = new RegExp(regExpString).test(value);

        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    function v_basicOperations(element, params, field, condition) {
        //逻辑运算a==b 算数运算htcszje==wtzjje+wtccdyje | ljzjzjje>0  //暂不支持括号运算
        let arr_c, arr, columnName, isValid;
        arr_c = condition.match(/(>=|<=|>|<|\+|\-|\*|\/)(?=(?:[^']*(?:'[^']*')?[^']*)*$)/g); //算数运算 排除引号内运算符
        arr = condition.split(/(==|!=|>=|<=|>|<|\+|\-|\*|\/)(?=(?:[^']*(?:'[^']*')?[^']*)*$)/g), columnName = arr[0].trim();
        //console.log("arr_c", arr_c, "arr", arr);
        for (let i = 0, len = arr.length; i < len; i++) {
            let str = arr[i];
            if (undefined !== element.form[str]) {
                if (null == arr_c) { // 逻辑运算 == != 均按照字符比较，因为数值类一般不使用这两个比较
                    condition = condition.replace(str, "'" + element.form[str].value.replace(",", "") + "'");
                } else { //算数运算
                    condition = condition.replace(str, element.form[str].value.replace(/,/g, "") || 0);
                }
            }
        }
        //console.log("basicOperations", condition);
        isValid = eval(condition);
        return {
            columnName: columnName,
            isValid: isValid,
        };
    }

    // 逻辑校验-前置条件校验
    function logicCheck_preCheck(element, params, field) {
        try {
            //console.log("logicCheck_preCheck", unescape(params[0]));
            return logicCheck_baseCheck(element, params, field, unescape(params[0]));
        } catch (e) {
            let preCondition = unescape(params[0]);
            let checkRule = unescape(params[1]);
            console.error("logicCheck_preCheck异常:", preCondition, checkRule, e);
            sAlert("逻辑校验-前置条件校验<br>" + preCondition, "异常");
        }
    }

    // 逻辑校验-规则校验
    function logicCheck_ruleCheck(element, params, field) {
        try {
            //console.log("logicCheck_ruleCheck", unescape(params[1]));
            return logicCheck_baseCheck(element, params, field, unescape(params[1]));
        } catch (e) {
            let preCondition = unescape(params[0]);
            let checkRule = unescape(params[1]);
            console.error("logicCheck_ruleCheck异常", preCondition, checkRule, e);
            sAlert("逻辑校验-后置规则校验<br>" + checkRule, "异常");
        }

    }

    // 逻辑校验-联动
    function logicCheck_linkage(element, params, field) {
        let preCondition = unescape(params[0]);
        let rule = unescape(params[1]);
        let ruleDesc = unescape(params[2]);
        //console.log("logicCheck_linkage", element.name, preCondition, rule, ruleDesc);
        // 分为两类,赋值类和比较类

        let columnName;

        // 赋值类

        // 先列特殊的,等价于==的
        if (rule.indexOf("isNull") != -1) {
            columnName = rule.replace(/isNull\(|\)/g, "");
            //进入页面第一次校验,不设置空值,这样可以看到不符合规定的字段并给予提示
            if ($(element.form).data("inited")) element.form[columnName].value = "";
            element.form[columnName].classList.add("readonly");
            $(element.form[columnName]).isValid(); //空值可能影响别的,需要校验
        } else if (/==/.test(rule)) {
            if (/^[^\+|\-|\*|\/]*==/.test(rule)) { // == 前没有 其他运算符
                if (!$(element.form).data("inited")) return;

                if (/\(.+?\)/.test(rule)) { // 有括号
                    if (/date\(.*?\)/.test(rule)) { // 日期处理
                        // date(cpjhdqr,'yyyy-MM-dd')比较
                        let arr = rule.match(/(?<=\()([^']+?)(?=,)|(?<=\('|,')([^']+?)(?=')/g);
                        columnName = arr[0];
                        if (/date\(.*?\)==date\([0-9\-]*?\)/.test(rule)) { // 赋值类
                            //date(cpjhdqr,'yyyy-MM-dd')==date('9999-12-31,'yyyy-MM-dd')
                            element.form[columnName].value = Date.parseDate(arr[2], arr[3]).format(arr[1]);
                            $(element.form[columnName]).isValid(); //值变化,需要校验
                        } else { //比较类
                            // 容易引起循环校验,暂不处理,可以写两条进行处理
                        }
                    } else if (/doubleValue.*==/g.test(rule)) { // 算数 在==前
                        //console.log(rule)
                        let condition = rule.split("==")[1];
                        let colNameArr = rule.match(/(?<=doubleValue\()(.+?)(?=\))/g); //获取所有数值字段
                        // 如果名称不规范,前后带有空格,将导致后续报错,规范书写即可
                        columnName = colNameArr[0];
                        for (let i = 0, len = colNameArr.length; i < len; i++) {
                            let v = element.form[colNameArr[i]].value.replace(/,/g, "") || 0;
                            condition = condition.replace("doubleValue(" + colNameArr[i] + ")", v);
                        }
                        let datascale = element.form[columnName].getAttribute("datascale");
                        //使用math.evaluate()运算,更简单
                        element.form[columnName].value = $.number(eval(math.evaluate(condition)), datascale);
                        $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                    }
                } else { //赋值
                    let arr = rule.split("==");
                    columnName = arr[0];
                    if (element.form[arr[1]]) { //双字段 后面字段赋值给前面字段
                        if (element.form[columnName].getAttribute("linkage_dict_column_post")) {
                            element.form[columnName].value = element.form[arr[1]].value;
                            // 触发change事件
                            let evt = document.createEvent("HTMLEvents"); //创建事件
                            evt.initEvent("change"); //初始化
                            element.form[columnName].dispatchEvent(evt); // 触发
                        } else if (element.form[columnName].getAttribute("linkage_dict_column_pre")) {
                            showLoading2("联动设置...");
                            window.setTimeout(function() {
                                element.form[columnName].value = element.form[arr[1]].value;
                                $(element.form[columnName]).isValid();
                                closeLoading2();
                            }, 1000);
                        } else {
                            element.form[columnName].value = element.form[arr[1]].value;
                        }
                    } else { // 字符串或固定数值赋值
                        element.form[columnName].value = eval(arr[1]);
                        element.form[columnName].classList.remove("readonly");
                        $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                    }
                }
                //$(element.form[columnName]).isValid();
            }

        } else { // 比较类
            // 先列特殊的,具有特殊含义的比较符
            if (rule.indexOf("isNotNull") != -1) {
                let paramArr = rule.match(/isNotNull\((.+?)\)/)[1].split(",");
                for (let i = 0, len = paramArr.length; i < len; i++) {
                    columnName = paramArr[i];
                    if (!/eq|ge/.test(columnName) && isNaN(columnName)) {
                        element.form[columnName].classList.remove("readonly");
                        $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                    }
                }
            } else if (rule.indexOf("isIn") != -1) {
                let paramArr = rule.match(/(?<=\()([^']+?)(?=,)|(?<=\('|,')([^']+?)(?=')/g);
                columnName = paramArr[0];
                element.form[columnName].classList.remove("readonly");
                //经常会前置条件包含自己未排除自身,还会导致可能存在的死循环
                //$(element.form[columnName]).isValid(); //校验，不通过则触发提醒
            } else if (rule.indexOf("optional") != -1) {
                columnName = rule.match(/optional\((.+?)\)/)[1];
                element.form[columnName].classList.remove("readonly");
                $(element.form[columnName]).trigger("showmsg", ["tip", ruleDesc]);
            } else { // 比较符号 >|>=|<=|<|!= 可能还有其他的
                let cols = new Array();
                $(element.form).find(":input:not(:button)").each(function(i, n) {
                    cols.push(n.name);
                });
                let colsReg = new RegExp(cols.join("|"), "g");
                let arr_pre = preCondition.match(colsReg);
                let arr = rule.match(colsReg);

                //循环,移除前置字段,避免循环触发
                for (let i = 0, len = arr_pre.length; i < len; i++) {
                    //arr.remove(arr_pre[i]); //不能完全剔除,使用循环
                    let j = arr.length;
                    while (j--) {
                        if (arr[j] == arr_pre[i]) {
                            arr.splice(j, 1);
                        }
                    }
                }
                //循环,触发字段校验
                for (let i = 0, len = arr.length; i < len; i++) {
                    $(element.form[arr[i]]).isValid();
                }

            }

        }
    }

    // 逻辑校验-联动 备份
    function logicCheck_linkage_20191226(element, params, field) {
        let preCondition = unescape(params[0]);
        let rule = unescape(params[1]);
        let ruleDesc = unescape(params[2]);
        //console.log("logicCheck_linkage", element.name, preCondition, rule, ruleDesc);
        let columnName;
        if (/!=/.test(rule)) { //!= 只需要校验被动字段，触发提示即可,放在第一位
            let cols = new Array();
            $(element.form).find(":input:not(:button)").each(function(i, n) {
                cols.push(n.name);
            });
            let colsReg = new RegExp(cols.join("|"), "g");
            let arr = rule.match(colsReg);
            for (let i = 0, len = arr.length; i < len; i++) {
                $(element.form[arr[i]]).isValid();
            }
        } else if (/date\(.*?\)/.test(rule)) { // 日期处理
            // date(cpjhdqr,'yyyy-MM-dd')比较
            let arr = rule.match(/(?<=\()([^']+?)(?=,)|(?<=\('|,')([^']+?)(?=')/g);
            columnName = arr[0];
            if (/date\(.*?\)==date\([0-9\-]*?\)/.test(rule)) { // 赋值类
                //date(cpjhdqr,'yyyy-MM-dd')==date('9999-12-31,'yyyy-MM-dd')
                element.form[columnName].value = Date.parseDate(arr[2], arr[3]).format(arr[1]);
                $(element.form[columnName]).isValid(); //值变化,需要校验
            } else { //比较类
                // 容易引起循环校验,暂不处理,可以写两条进行处理
            }
        } else if (rule.indexOf("isNull") != -1) {
            columnName = rule.replace(/isNull\(|\)/g, "");
            //进入页面第一次校验,不设置空值,这样可以看到不符合规定的字段并给予提示
            if ($(element.form).data("inited")) element.form[columnName].value = "";
            element.form[columnName].classList.add("readonly");
            $(element.form[columnName]).isValid(); //空值可能影响别的,需要校验
        } else if (rule.indexOf("isNotNull") != -1) {
            let paramArr = rule.match(/isNotNull\((.+?)\)/)[1].split(",");
            for (let i = 0, len = paramArr.length; i < len; i++) {
                columnName = paramArr[i];
                if (isNaN(columnName)) {
                    element.form[columnName].classList.remove("readonly");
                    $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                }
            }
        } else if (rule.indexOf("isIn") != -1) {
            let paramArr = rule.match(/(?<=\()([^']+?)(?=,)|(?<=\('|,')([^']+?)(?=')/g);
            columnName = paramArr[0];
            element.form[columnName].classList.remove("readonly");
            $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
        } else if (rule.indexOf("optional") != -1) {
            columnName = rule.match(/optional\((.+?)\)/)[1];
            element.form[columnName].classList.remove("readonly");
            $(element.form[columnName]).trigger("showmsg", ["tip", ruleDesc]);
        } else if (/^[^\+|\-|\*|\/]*==/.test(rule)) { // == 前没有 其他运算符
            if (!$(element.form).data("inited")) return;
            if (/\(.+?\)/.test(rule)) { // 有括号
                if (/doubleValue.*==/g.test(rule)) { // 算数 在==前
                    let condition = rule.split("==")[1];
                    let colNameArr = rule.match(/(?<=doubleValue\()(.+?)(?=\))/g); //获取所有数值字段
                    // 如果名称不规范,前后带有空格,将导致后续报错,规范书写即可
                    columnName = colNameArr[0];
                    for (let i = 0, len = colNameArr.length; i < len; i++) {
                        let v = element.form[colNameArr[i]].value.replace(/,/g, "") || 0;
                        condition = condition.replace("doubleValue(" + colNameArr[i] + ")", v);
                    }
                    condition = getNewConditionOfDecimal(condition); // 获取升幂降幂后的condition,避免精度丢失问题
                    let datascale = element.form[columnName].getAttribute("datascale");
                    element.form[columnName].value = $.number(eval(condition), datascale);
                    $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                }
            } else { //赋值
                let arr = rule.split("==");
                columnName = arr[0];
                if (element.form[arr[1]]) { //双字段 后面字段赋值给前面字段
                    if (element.form[columnName].getAttribute("linkage_dict_column_post")) {
                        element.form[columnName].value = element.form[arr[1]].value;
                        // 触发change事件
                        let evt = document.createEvent("HTMLEvents"); //创建事件
                        evt.initEvent("change"); //初始化
                        element.form[columnName].dispatchEvent(evt); // 触发
                    } else if (element.form[columnName].getAttribute("linkage_dict_column_pre")) {
                        showLoading2("联动设置...");
                        window.setTimeout(function() {
                            element.form[columnName].value = element.form[arr[1]].value;
                            $(element.form[columnName]).isValid();
                            closeLoading2();
                        }, 1000);
                    } else {
                        element.form[columnName].value = element.form[arr[1]].value;
                    }
                } else { // 字符串或固定数值赋值
                    element.form[columnName].value = eval(arr[1]);
                    element.form[columnName].classList.remove("readonly");
                    $(element.form[columnName]).isValid(); //校验，不通过则触发提醒
                }
            }
            $(element.form[columnName]).isValid();
        } else {
            //console.log("未发现匹配的处理规则,请书写对应JavaScript代码", preCondition, rule, ruleDesc);
            //$(element.form[columnName]).isValid();
            //return "未发现匹配的处理规则,请书写对应JavaScript代码";
        }
    }

    /* Themes
     */
    let TPL_ARROW = "<span class=\"n-arrow\"><b>◆</b><i>◆</i></span>";
    $.validator.setTheme({
        "simple_right": {
            formClass: "n-simple",
            msgClass: "n-right",
        },
        "simple_bottom": {
            formClass: "n-simple",
            msgClass: "n-bottom",
        },
        "yellow_top": {
            formClass: "n-yellow",
            msgClass: "n-top",
            msgArrow: TPL_ARROW,
        },
        "yellow_right": {
            formClass: "n-yellow",
            msgClass: "n-right",
            msgArrow: TPL_ARROW,
        },
        "yellow_right_effect": {
            formClass: "n-yellow",
            msgClass: "n-right",
            msgArrow: TPL_ARROW,
            msgShow: function($msgbox, type) {
                let $el = $msgbox.children();
                if ($el.is(":animated")) return;
                if (type === "error") {
                    $el.css({
                            left: "20px",
                            opacity: 0,
                        })
                        .delay(100).show().stop()
                        .animate({
                            left: "-4px",
                            opacity: 1,
                        }, 150)
                        .animate({
                            left: "3px",
                        }, 80)
                        .animate({
                            left: 0,
                        }, 80);
                } else {
                    $el.css({
                        left: 0,
                        opacity: 1,
                    }).fadeIn(200);
                }
            },
            msgHide: function($msgbox, type) {
                let $el = $msgbox.children();
                $el.stop().delay(100).show()
                    .animate({
                        left: "20px",
                        opacity: 0,
                    }, 300, function() {
                        $msgbox.hide();
                    });
            },
        },
    });
}));
