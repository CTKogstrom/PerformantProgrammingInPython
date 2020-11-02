use std::slice;

#[no_mangle]
pub extern fn cipher(msg: *const i8, key: *const i8, buf: *mut i8, msg_len: usize, key_len: usize){

    let full_msg = unsafe{slice::from_raw_parts(msg, msg_len)};
    let full_key = unsafe{slice::from_raw_parts(key, key_len)};
    let full_buf = unsafe{slice::from_raw_parts_mut(buf, msg_len)};


    for i in 0..msg_len as usize {
        full_buf[i] = full_msg[i] ^ full_key[i % key_len];
    };

}