package com.deconest.common.security;

public interface PasswordHasher {

    String hash(String rawPassword);
}

