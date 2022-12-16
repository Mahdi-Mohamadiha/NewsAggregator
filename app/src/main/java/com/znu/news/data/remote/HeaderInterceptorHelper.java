package com.znu.news.data.remote;

import androidx.annotation.NonNull;

import java.io.IOException;

import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

public class HeaderInterceptorHelper implements Interceptor {

    private String token = null;

    public HeaderInterceptorHelper(String token) {
        this.token = token;
    }

    @NonNull
    @Override
    public Response intercept(@NonNull Chain chain) throws IOException {
        Request request = chain.request().newBuilder().addHeader("token", token).build();
        return chain.proceed(request);
    }
}
