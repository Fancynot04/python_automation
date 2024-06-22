/*********************************
 * Themes, rules, and i18n support
 * Locale: Chinese; 中文
 * function: 1.Basic logic for checking if a numeric string falls within a specified  
 *           range
 *           2.The three types of validation for input data are basic validation,
 *           logical validation,cross-table validation 
 * digits: [/^\d+$/, "请填写数字"],
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
            password: [/^[\S]{6,16}$/, "请填写6-16位字符，不能包含空格"]
 *********************************/

