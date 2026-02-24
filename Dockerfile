FROM python:3.13-alpine3.22

RUN adduser -h /code -u 1000 -D -H api

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --chown=api:api requirements.txt /code/requirements.txt
COPY --chown=api:api /code            /code

WORKDIR /code
ENV PATH="/code/.local/bin:${PATH}"

RUN su api -c "pip3 install --break-system-packages --user -U -r requirements.txt" \
    && rm requirements.txt

USER api

# Expose port (using the default port from README)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/check || exit 1

# Run the application with gunicorn
CMD ["python", "/code/app.py"]
