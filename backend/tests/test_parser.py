from app.services.code_parser import parse_code

def test_parse_python_code():
    code = """
'''Module docstring'''
import os
from math import sqrt

class Calculator:
    def add(self, a, b):
        return a + b

def multiply(a, b):
    return a * b
"""
    result = parse_code("calc.py", code)
    assert result["language"] == "python"
    assert "Calculator" in result["classes"]
    assert "multiply" in result["functions"]
    assert "os" in result["dependencies"]

def test_parse_js_ts_code():
    code = """
import React from 'react';
const axios = require('axios');

class Header extends React.Component {
    render() {
        return <h1>Hello</h1>;
    }
}

export const fetchUsers = () => {
    return axios.get('/users');
}
"""
    result = parse_code("Header.tsx", code)
    assert result["language"] == "typescript"
    assert "Header" in result["classes"]
    assert "fetchUsers" in result["functions"]
    assert "react" in result["dependencies"]
    assert "axios" in result["dependencies"]

def test_parse_go_code():
    code = """
package main

import (
    "fmt"
    "net/http"
)

func runServer() {
    fmt.Println("Running...")
}
"""
    result = parse_code("main.go", code)
    assert result["language"] == "go"
    assert "runServer" in result["functions"]
    assert "fmt" in result["dependencies"]
    assert "net/http" in result["dependencies"]
