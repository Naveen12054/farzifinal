package com.deconest.bootstrap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@EnableJpaAuditing
@EntityScan(basePackages = "com.deconest")
@EnableJpaRepositories(basePackages = "com.deconest")
@SpringBootApplication(scanBasePackages = "com.deconest")
public class DecoNestApplication {

    public static void main(String[] args) {
        SpringApplication.run(DecoNestApplication.class, args);
    }
}
