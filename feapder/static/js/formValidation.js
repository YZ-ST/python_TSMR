// 檢核出發站不可等於抵達站
function checkStation() {
  if (depart_station.value == arrive_station.value) {
    check_arrive_station.innerHTML = "[出發站]不可等於[抵達站]";
    depart_station.style.backgroundColor = "pink";
    arrive_station.style.backgroundColor = "pink";
    return false;
  } else {
    check_arrive_station.innerHTML = "";
    depart_station.style.backgroundColor = "white";
    arrive_station.style.backgroundColor = "white";
    return true;
  }
}

// 檢核日期
function checkDate() {
  if (book_ticket_time.value == "") {
    book_ticket_time.style.backgroundColor = "pink";
    check_book_ticket_time.innerHTML = "請輸入出發日期";
    return false;
  }
  // 檢核日期格式
  if (book_ticket_time.value != "") {
    checkLine1 = book_ticket_time.value.substr(4, 1) != "-";
    checkLine2 = book_ticket_time.value.substr(7, 1) != "-";
    checkLength = book_ticket_time.value.length != 10;

    if (checkLine1 || checkLine2 || checkLength) {
      book_ticket_time.style.backgroundColor = "pink";
      check_book_ticket_time.innerHTML = "輸入格式應為：XXXX-XX-XX";
      return false;
    } else {
      book_ticket_time.style.backgroundColor = "white";
      check_book_ticket_time.innerHTML = "";
    }

    // 檢核日期是否介於今日及29天內
    // 在高鐵票務通路預訂29天內(含乘車當日)之車票；每逢週五及週六至多可預訂四週後至週日之車票
    var today = new Date();
    var bookingDate = new Date(book_ticket_time.value);
    var daysOfWeek = ["7", "1", "2", "3", "4", "5", "6"];
    var dayOfWeek = daysOfWeek[today.getDay()];
    if (getDateFormat(bookingDate) < getDateFormat(today)) {
      book_ticket_time.style.backgroundColor = "pink";
      check_book_ticket_time.innerHTML =
        "<br>不可早於今日 (" + getDateFormat(today) + ")";
      return false;
    }
    var addDate = 28;
    if (dayOfWeek == "5") {
      addDate += 3;
    } else if (dayOfWeek == "6") {
      addDate += 2;
    }
    var endDateLimit = new Date();
    endDateLimit.setDate(new Date().getDate() + addDate);
    if (getDateFormat(bookingDate) > getDateFormat(endDateLimit)) {
      book_ticket_time.style.backgroundColor = "pink";
      check_book_ticket_time.innerHTML =
        "<br>不可晚於 " + getDateFormat(endDateLimit);
      return false;
    } else {
      book_ticket_time.style.backgroundColor = "white";
      check_book_ticket_time.innerHTML = "";
      return true;
    }
  }
}

// 轉換日期格式
function getDateFormat(date) {
  var year = date.getFullYear();
  var month = (date.getMonth() + 1).toString().padStart(2, "0"); // 月份需要加1，且确保两位数显示
  var day = date.getDate().toString().padStart(2, "0"); // 确保日期以两位数显示
  return year + "-" + month + "-" + day;
}

// 變更結束日期
function changeDepartTime() {
  end_time.value = depart_time.value;
  checkEndTime();
}

// 檢核預計最早時間是否小於預計最晚時間
function checkEndTime() {
  if (
    depart_time.value != end_time.value &&
    (depart_time.value.substr(0, 2) > end_time.value.substr(0, 2) ||
      (depart_time.value.substr(0, 2) == end_time.value.substr(0, 2) &&
        depart_time.value.substr(3, 2) > end_time.value.substr(3, 2)))
  ) {
    check_depart_time.innerHTML = "[最晚時間]不應早於[最早時間]";
    depart_time.style.backgroundColor = "pink";
    end_time.style.backgroundColor = "pink";
    return false;
  } else {
    check_depart_time.innerHTML = "";
    depart_time.style.backgroundColor = "white";
    end_time.style.backgroundColor = "white";
    return true;
  }
}

// 檢核身分證格式：第1碼為英文字母，後9位為數字，共10位數
function checkNationalId() {
  if (national_ID.value == "") {
    national_ID.style.backgroundColor = "pink";
    check_national_ID.innerHTML = "請輸入身分證號";
    return false;
  }
  if (national_ID.value.length != 10) {
    national_ID.style.backgroundColor = "pink";
    check_national_ID.innerHTML = "長度應為10碼";
    return false;
  } else if (!/[a-zA-Z]/.test(national_ID.value.substr(0, 1))) {
    national_ID.style.backgroundColor = "pink";
    check_national_ID.innerHTML = "第1碼應為字母";
    return false;
  } else if (!/^\d+$/.test(national_ID.value.substr(1, 9))) {
    national_ID.style.backgroundColor = "pink";
    check_national_ID.innerHTML = "第2碼~第10碼應為數字";
    return false;
  } else {
    check_national_ID.innerHTML = "";
    national_ID.style.backgroundColor = "white";
    return true;
  }
}

// 檢核電話號碼：09開頭，共10碼，皆數字
function checkPhoneNumber() {
  if (phonenumber.value != "") {
    if (phonenumber.value.length != 10) {
      phonenumber.style.backgroundColor = "pink";
      check_phonenumber.innerHTML = "應為10位數";
      return false;
    } else if (!/^\d+$/.test(phonenumber.value)) {
      phonenumber.style.backgroundColor = "pink";
      check_phonenumber.innerHTML = "應為10位數的數字";
      return false;
    } else if (phonenumber.value.substring(0, 2) != "09") {
      phonenumber.style.backgroundColor = "pink";
      check_phonenumber.innerHTML = "應為09開頭";
      return false;
    } else {
      phonenumber.style.backgroundColor = "white";
      check_phonenumber.innerHTML = "";
      return true;
    }
  }
  return true;
}

// 檢核電子信箱格式
function checkEmail() {
  var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (email.value != "") {
    if (!emailPattern.test(email.value)) {
      check_email.innerHTML = "請輸入有效的電子信箱";
      email.style.backgroundColor = "pink";
      return false;
    } else {
      check_email.innerHTML = "";
      email.style.backgroundColor = "white";
      return true;
    }
  }
  return true;
}

// 檢核 TGo 帳號：2位大寫英文+8位數字
function checkTGo() {
  if (to_go_account.value != "") {
    if (to_go_account.value.length != 10) {
      to_go_account.style.backgroundColor = "pink";
      check_to_go_account.innerHTML = "格式應為2位大寫英文+8位數字";
      return false;
    } else if (!/^[A-Za-z]+$/.test(to_go_account.value.substr(0, 2))) {
      to_go_account.style.backgroundColor = "pink";
      check_to_go_account.innerHTML = "前2位應為英文字母";
      return false;
    } else if (!/^\d+$/.test(to_go_account.value.substr(2, 8))) {
      to_go_account.style.backgroundColor = "pink";
      check_to_go_account.innerHTML = "後8位應為數字";
      return false;
    } else {
      to_go_account.style.backgroundColor = "white";
      check_to_go_account.innerHTML = "";
      return true;
    }
  }
  return true;
}

// 提交前檢核表單欄位
function validateForSave() {
  var totalErrMsg = "";
  // 檢核必填欄位是否皆有值：出發日期、身分證號
  if (book_ticket_time.value == "" && national_ID.value != "") {
    totalErrMsg += "請輸入[出發日期]";
    book_ticket_time.style.backgroundColor = "pink";
    national_ID.style.backgroundColor = "white";
    return false;
  } else if (book_ticket_time.value != "" && national_ID.value == "") {
    totalErrMsg += "請輸入[身分證號]";
    book_ticket_time.style.backgroundColor = "white";
    national_ID.style.backgroundColor = "pink";
    return false;
  } else if (book_ticket_time.value == "" && national_ID.value == "") {
    totalErrMsg += "請輸入[身分證號]及[出發日期]";
    book_ticket_time.style.backgroundColor = "pink";
    national_ID.style.backgroundColor = "pink";
    return false;
  }

  // 再次檢核所有欄位
  if (!checkStation()) {
    totalErrMsg += "[出發站]不可等於[抵達站]<br>";
  }
  if (!checkDate()) {
    totalErrMsg += "[出發日期]格式有誤或不在可訂票日期範圍內<br>";
  }
  if (!checkEndTime()) {
    totalErrMsg += "[最晚時間]不應早於[最早時間]<br>";
  }
  if (!checkNationalId()) {
    totalErrMsg += "[身分證號]格式有誤<br>";
  }
  if (!checkPhoneNumber() && phonenumber.value != "") {
    totalErrMsg += "[電話]格式有誤<br>";
  }
  if (!checkEmail() && email.value != "") {
    totalErrMsg += "[電子信箱]格式有誤<br>";
  }
  if (!checkTGo() && to_go_account.value != "") {
    totalErrMsg += "[TGo帳號]格式有誤<br>";
  }

  if (totalErrMsg != "") {
    finalErrMsg.style.display = "";
    finalErrMsg.innerHTML = totalErrMsg;
    return false;
  } else {
    finalErrMsg.style.display = "none";
    totalErrMsg = "";
    return true;
  }
}
